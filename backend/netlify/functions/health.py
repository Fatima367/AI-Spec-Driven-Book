import json


def handler(event, context):
    """
    Netlify Function handler for health check endpoint
    """
    try:
        response = {
            "status": "healthy",
            "version": "1.0.0",
            "timestamp": context.aws_request_id if hasattr(context, 'aws_request_id') else "unknown"
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response)
        }

    except Exception as e:
        print(f"Health check error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'status': 'unhealthy', 'error': str(e)})
        }