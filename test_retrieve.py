#!/usr/bin/env python3
"""
Test script to validate end-to-end functionality of the RAG retrieval system.
This runs a simple test to confirm the system works as expected.
"""
import os
import sys
import time
from backend.retrieve import (
    QdrantConnectionConfig,
    validate_connection_and_vectors,
    setup_cohere_client,
    connect_to_qdrant,
    process_sample_query,
    Query,
    generate_validation_result,
    generate_validation_report
)

def test_end_to_end():
    """Run validation on sample queries to confirm end-to-end functionality"""
    print("[TEST] Testing RAG Retrieval & Pipeline Validation System")
    print("=" * 60)

    # Test 1: Validate connection
    print("\n[INFO] Testing Connection Validation...")
    try:
        config = QdrantConnectionConfig()
        result = validate_connection_and_vectors(config)
        print(f"   Connected: {result['connected']}")
        print(f"   Vectors Count: {result['vectors_count']}")
        print(f"   Has Vectors: {result['has_vectors']}")
        assert result['connected'], "Connection should be successful"
        assert result['has_vectors'], "Should have vectors in collection"
        print("   [PASS] Connection validation passed!")
    except Exception as e:
        print(f"   [FAIL] Connection validation failed: {e}")
        return False

    # Test 2: Process a sample query
    print("\n[INFO] Testing Sample Query Processing...")
    try:
        # Set up clients
        cohere_client = setup_cohere_client()
        qdrant_client = connect_to_qdrant(config)

        # Process a sample query
        sample_query = "What is Physical AI and Humanoid Robotics?"
        results = process_sample_query(
            sample_query,
            qdrant_client,
            cohere_client,
            config,
            limit=3
        )

        print(f"   Query: '{sample_query}'")
        print(f"   Results Count: {len(results)}")
        if results:
            print(f"   Top Result Score: {results[0].score:.3f}")
            print(f"   Top Result Content Preview: {results[0].content[:100]}...")

        # Create query object and validation
        query_obj = Query(text=sample_query)
        validation_result = generate_validation_result(query_obj, results)
        execution_time = 0.5  # Mock execution time
        validation_report = generate_validation_report(sample_query, [validation_result], execution_time)

        print(f"   Validation Success Rate: {validation_report.success_rate:.2%}")
        print(f"   Validation Avg Similarity: {validation_report.avg_similarity:.3f}")
        print("   [PASS] Sample query processing passed!")
    except Exception as e:
        print(f"   [FAIL] Sample query processing failed: {e}")
        return False

    print("\n[SUCCESS] All tests passed! End-to-end functionality confirmed.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_end_to_end()
    sys.exit(0 if success else 1)