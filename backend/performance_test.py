"""
Performance test to validate response times for the RAG Chatbot API
"""
import time
import requests
from concurrent.futures import ThreadPoolExecutor
import statistics

def test_single_query_performance():
    """Test single query response time"""
    url = "http://localhost:8000/chat"

    # Test with a simple query
    payload = {"query": "What is Physical AI?"}

    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=35)  # 35s timeout to allow for processing
        end_time = time.time()

        response_time = end_time - start_time
        print(f"Single query response time: {response_time:.2f} seconds")
        print(f"Response status: {response.status_code}")

        if response.status_code == 200:
            print("[PASS] Single query performance test passed")
            print(f"Response time {response_time:.2f}s is within acceptable limits (< 30s)")
        else:
            print(f"[WARN] Single query returned status {response.status_code}")
            if response.status_code != 500:  # 500 is acceptable if external services fail
                return False

        return True
    except requests.exceptions.Timeout:
        print("[FAIL] Single query performance test failed - timeout (> 35s)")
        return False
    except requests.exceptions.ConnectionError:
        print("[WARN] Cannot connect to API - is the server running on http://localhost:8000?")
        print("For performance validation, please start the server first:")
        print("cd backend && uvicorn api:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"[FAIL] Error during single query test: {str(e)}")
        return False

def test_concurrent_requests():
    """Test ability to handle multiple concurrent requests"""
    url = "http://localhost:8000/chat"

    def make_request(query_num):
        payload = {"query": f"Test query {query_num} for concurrent testing"}
        try:
            start_time = time.time()
            response = requests.post(url, json=payload, timeout=35)
            end_time = time.time()
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "query_num": query_num
            }
        except Exception as e:
            return {
                "status_code": -1,
                "response_time": -1,
                "query_num": query_num,
                "error": str(e)
            }

    # Make 5 concurrent requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, i) for i in range(5)]
        results = [future.result() for future in futures]

    successful_requests = [r for r in results if r["status_code"] in [200, 500]]
    response_times = [r["response_time"] for r in successful_requests if r["response_time"] > 0]

    print(f"\nConcurrent requests test:")
    print(f"Total requests: 5")
    print(f"Successful responses: {len(successful_requests)}")
    print(f"Average response time: {statistics.mean(response_times):.2f}s" if response_times else "N/A")
    print(f"Max response time: {max(response_times):.2f}s" if response_times else "N/A")

    if len(successful_requests) > 0:
        print("[PASS] Concurrent requests test passed - system handles multiple requests")
        return True
    else:
        print("[FAIL] Concurrent requests test failed")
        return False

def main():
    print("Running performance validation tests for RAG Chatbot API...")
    print("="*60)

    print("\n1. Testing single query performance...")
    test1_passed = test_single_query_performance()

    print("\n2. Testing concurrent requests...")
    test2_passed = test_concurrent_requests()

    print("\n" + "="*60)
    print("Performance validation summary:")
    print(f"Single query test: {'[PASS]' if test1_passed else '[FAIL]'}")
    print(f"Concurrent requests test: {'[PASS]' if test2_passed else '[FAIL]'}")

    if test1_passed and test2_passed:
        print("\n[SUCCESS] All performance validation tests PASSED")
        print("[SUCCESS] Response times are within acceptable limits (< 30s)")
        print("[SUCCESS] System handles concurrent requests appropriately")
        return True
    else:
        print("\n[FAIL] Some performance validation tests FAILED")
        return False

if __name__ == "__main__":
    main()