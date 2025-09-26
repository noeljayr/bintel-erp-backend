import math
from django.db.models import Q, Count
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes
from openpyxl import Workbook
from .models import Request
from .serializers import RequestSerializer, RequestCreateSerializer, RequestUpdateSerializer, RequestEditSerializer, RequestListResponseSerializer
from apps.users.models import User

@extend_schema(
    tags=['Requests'],
    summary='List requests or create new request',
    description='GET: Retrieve paginated list of requests with filtering and search. POST: Create a new request.',
    parameters=[
        OpenApiParameter('status', str, description='Filter by status', enum=['Pending', 'Approved', 'Rejected']),
        OpenApiParameter('page', int, description='Page number for pagination'),
        OpenApiParameter('limit', int, description='Number of items per page'),
        OpenApiParameter('search', str, description='Search in purpose, amount, or user names'),
    ],
    request=RequestCreateSerializer,
    responses={
        200: RequestListResponseSerializer,
        201: RequestSerializer,
    },
    examples=[
        OpenApiExample(
            'Create Request',
            value={
                "amount": 1500.00,
                "currency": "USD",
                "approver_id": "123e4567-e89b-12d3-a456-426614174000",
                "purpose": "Office supplies purchase",
                "description": "Need to buy new laptops for the team",
                "required_on": "2024-02-15"
            }
        )
    ]
)
@api_view(['GET', 'POST'])
def requests_list_create(request):
    if request.method == 'GET':
        return get_requests(request)
    elif request.method == 'POST':
        return create_request(request)

def get_requests(request):
    status_filter = request.query_params.get('status')
    page = int(request.query_params.get('page', 1))
    limit = int(request.query_params.get('limit', 10))
    search = request.query_params.get('search', '').strip()
    
    # Base filter
    filters = Q()
    
    # Filter by status
    if status_filter:
        filters &= Q(status=status_filter)
    
    # Role-based access control
    if request.user_data['role'] != 'Partner':
        filters &= Q(request_by=request.user_data['id'])
    
    # Search functionality
    if search:
        search_filters = Q(purpose__icontains=search)
        
        # Amount search
        try:
            amount_value = float(search)
            search_filters |= Q(amount=amount_value)
        except ValueError:
            pass
        
        # Name search
        matched_users = User.objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search)
        ).values_list('user_id', flat=True)
        
        if matched_users:
            search_filters |= Q(request_by__in=matched_users) | Q(approver_id__in=matched_users)
        
        filters &= search_filters
    
    # Get total count and requests
    total = Request.objects.filter(filters).count()
    
    # Pagination
    offset = (page - 1) * limit
    requests = Request.objects.filter(filters)[offset:offset + limit]
    
    # Status counts (with role-based access)
    status_base_filter = Q()
    if request.user_data['role'] != 'Partner':
        status_base_filter = Q(request_by=request.user_data['id'])
    
    status_counts = Request.objects.filter(status_base_filter).values('status').annotate(count=Count('status'))
    status_summary = {'Pending': 0, 'Approved': 0, 'Rejected': 0}
    for item in status_counts:
        status_summary[item['status']] = item['count']
    
    # Serialize requests
    serializer = RequestSerializer(requests, many=True)
    
    return Response({
        'page': page,
        'limit': limit,
        'total': total,
        'totalPages': math.ceil(total / limit),
        'statusCounts': status_summary,
        'data': serializer.data
    })

@extend_schema(
    tags=['Requests'],
    summary='Export approved requests',
    description='Download Excel file containing all approved requests',
    responses={
        200: OpenApiResponse(
            response=OpenApiTypes.BINARY,
            description='Excel file download'
        )
    }
)
@api_view(['GET'])
def export_requests(request):
    # Only approved requests
    filters = Q(status='Approved')
    
    # Role-based access control
    if request.user_data['role'] != 'Partner':
        filters &= Q(request_by=request.user_data['id'])
    
    requests = Request.objects.filter(filters).order_by('-initiated_on')
    
    # Create workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'Approved Requests'
    
    # Headers
    headers = ['Requested By', 'Amount', 'Approved By', 'Purpose', 'Date']
    ws.append(headers)
    
    # Data rows
    for req in requests:
        try:
            requester = User.objects.get(user_id=req.request_by)
            requester_name = f"{requester.first_name} {requester.last_name}"
        except User.DoesNotExist:
            requester_name = "Unknown"
        
        try:
            approver = User.objects.get(user_id=req.approver_id)
            approver_name = f"{approver.first_name} {approver.last_name}"
        except User.DoesNotExist:
            approver_name = "Unknown"
        
        ws.append([
            requester_name,
            f"{req.currency} {req.amount:,.2f}",
            approver_name,
            req.purpose,
            req.initiated_on.strftime('%Y-%m-%d')
        ])
    
    # Create response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="approved-requests.xlsx"'
    
    wb.save(response)
    return response

@extend_schema(
    tags=['Requests'],
    summary='Get, update, or delete request',
    description='GET: Retrieve detailed information about a specific request. PATCH: Update request status (approvers only) or edit request details (requesters only for pending requests). DELETE: Delete pending requests (requesters only).',
    responses={
        200: RequestSerializer,
        204: OpenApiResponse(description='Request deleted successfully'),
        400: OpenApiResponse(description='Bad request - cannot modify non-pending request'),
        403: OpenApiResponse(description='Forbidden - not authorized'),
        404: OpenApiResponse(description='Request not found')
    },
    examples=[
        OpenApiExample(
            'Update Status (Approver)',
            value={"status": "Approved"}
        ),
        OpenApiExample(
            'Edit Request (Requester - Pending Only)',
            value={
                "amount": 2000.00,
                "currency": "USD",
                "purpose": "Updated office supplies purchase",
                "description": "Updated description",
                "required_on": "2024-03-01"
            }
        )
    ]
)
@api_view(['GET', 'PATCH', 'DELETE', 'PUT'])
def request_detail_update(request, request_id):
    if request.method == 'GET':
        return get_request_by_id(request, request_id)
    elif request.method == 'PATCH':
        return update_request_status(request, request_id)
    elif request.method == 'PUT':
        return edit_request(request, request_id)
    elif request.method == 'DELETE':
        return delete_request(request, request_id)

def get_request_by_id(request, request_id):
    try:
        req = Request.objects.get(id=request_id)
    except Request.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Access control
    if request.user_data['role'] != 'Partner' and str(req.request_by) != request.user_data['id']:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = RequestSerializer(req)
    return Response(serializer.data)

def create_request(request):
    serializer = RequestCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Create request with current user as requester
    req = serializer.save(request_by=request.user_data['id'])
    
    # Return with populated data
    response_serializer = RequestSerializer(req)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

def update_request_status(request, request_id):
    try:
        req = Request.objects.get(id=request_id)
    except Request.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Only the approver can update status
    if request.user_data['id'] != str(req.approver_id):
        return Response({'error': 'Not authorized to update status'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = RequestUpdateSerializer(req, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    # Return updated request with populated data
    response_serializer = RequestSerializer(req)
    return Response(response_serializer.data)

def edit_request(request, request_id):
    """Edit request details (only for pending requests by the requester)"""
    try:
        req = Request.objects.get(id=request_id)
    except Request.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Only the requester can edit their own request
    if request.user_data['id'] != str(req.request_by):
        return Response({'error': 'Not authorized to edit this request'}, status=status.HTTP_403_FORBIDDEN)
    
    # Only pending requests can be edited
    if req.status != 'Pending':
        return Response({
            'error': f'Cannot edit request with status "{req.status}". Only pending requests can be edited.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create serializer for editing (allows more fields than status update)
    serializer = RequestEditSerializer(req, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    # Return updated request with populated data
    response_serializer = RequestSerializer(req)
    return Response(response_serializer.data)

def delete_request(request, request_id):
    """Delete request (only for pending requests by the requester)"""
    try:
        req = Request.objects.get(id=request_id)
    except Request.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Only the requester can delete their own request
    if request.user_data['id'] != str(req.request_by):
        return Response({'error': 'Not authorized to delete this request'}, status=status.HTTP_403_FORBIDDEN)
    
    # Only pending requests can be deleted
    if req.status != 'Pending':
        return Response({
            'error': f'Cannot delete request with status "{req.status}". Only pending requests can be deleted.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete the request
    req.delete()
    
    return Response({'message': 'Request deleted successfully'}, status=status.HTTP_204_NO_CONTENT)