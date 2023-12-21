import unittest
import os
import convogen
import json

class TestMemoizeWithProbability(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMemoizeWithProbability, self).__init__(*args, **kwargs)
        self.cache_file = 'test_cache.json'


    def setUp(self):
        # Ensure the cache file is removed before each test
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)


    def tearDown(self):
        # Clean up: remove the cache file after each test
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)


    def test_memoization(self):
        @convogen.memoize_with_probability(self.cache_file)
        def test_function(x):
            return x * 2

        # First call, should not be from cache
        result1 = test_function(5)
        self.assertEqual(result1, 10)

        # Second call, might be from cache
        result2 = test_function(5)
        self.assertIn(result2, [10, 5 * 2])  # Either cached or recalculated


    def test_memoization_with_json_cache(self):
        @convogen.memoize_with_probability(self.cache_file)
        def test_function(x):
            return x * 2

        # Call the function to potentially cache the result
        test_function(5)

        # Check if the cache file exists
        self.assertTrue(
                os.path.exists(self.cache_file),
                "Cache file not created")

        # Read the cache file and verify its content
        with open(self.cache_file, 'r') as file:
            cache = json.load(file)
            cache_key = repr(('test_function', (5,), tuple()))
            self.assertIn(cache_key, cache, "Cache does not contain the expected key")
            self.assertEqual(cache[cache_key], 10, "Cached value is incorrect")


if __name__ == '__main__':
    unittest.main()

