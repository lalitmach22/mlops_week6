-- Load testing script for Iris API prediction endpoint
-- This script is used by wrk to perform load testing

wrk.method = "POST"
wrk.body   = '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
wrk.headers["Content-Type"] = "application/json"

-- Function called at the beginning of the test
function init(args)
   print("Starting load test for Iris API...")
end

-- Function called for each request (optional customization)
function request()
   -- Can customize individual requests here if needed
   return wrk.format()
end

-- Function called when each response is received
function response(status, headers, body)
   -- Can process responses here if needed
   if status ~= 200 then
      print("Error response: " .. status .. " - " .. body)
   end
end

-- Function called at the end of the test
function done(summary, latency, requests)
   print("\n=== Load Test Summary ===")
   print("Duration: " .. summary.duration .. " seconds")
   print("Total requests: " .. summary.requests)
   print("Total errors: " .. summary.errors.connect + summary.errors.read + summary.errors.write + summary.errors.status + summary.errors.timeout)
   print("Requests/sec: " .. string.format("%.2f", summary.requests / (summary.duration / 1000000)))
   print("Average latency: " .. string.format("%.2f", latency.mean / 1000) .. "ms")
   print("50th percentile: " .. string.format("%.2f", latency:percentile(50) / 1000) .. "ms")
   print("90th percentile: " .. string.format("%.2f", latency:percentile(90) / 1000) .. "ms")
   print("99th percentile: " .. string.format("%.2f", latency:percentile(99) / 1000) .. "ms")
end
