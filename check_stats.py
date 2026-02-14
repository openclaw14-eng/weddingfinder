import httpx

url = 'https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/rpc/exec'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU',
    'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdxbHByd3Vyc2diZ2tma3d6a3liIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MDc1NzEzNSwiZXhwIjoyMDg2MzMzMTM1fQ.Nv1_gzB0Q5PrdiBO9Bn1CwQCLXh5BsivrG22HbN6wqU',
    'Content-Type': 'application/json'
}

sql = """
CREATE OR REPLACE FUNCTION public.get_stats()
RETURNS json AS $$
DECLARE
  result json;
BEGIN
  SELECT json_build_object(
    'vendor_count', (SELECT count(*) FROM vendors),
    'category_count', (SELECT count(*) FROM categories),
    'portal_count', (SELECT count(*) FROM portals)
  ) INTO result;
  RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
"""

httpx.post(url, json={'query': sql}, headers=headers)
r = httpx.post('https://gqlprwursgbgkfkwzkyb.supabase.co/rest/v1/rpc/get_stats', headers=headers)
print(r.text)
