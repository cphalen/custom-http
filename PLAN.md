# Lesson Plan

### Steps

1. Look at `main.py`: who can tell me what the `app` variable is actually doing here.
2. What if we removed FastAPI from the equation and did it on our own so we understood how it worked?
3. What is the HTTP model? Request-response means what?
4. Who can tell me what an HTTP request actually is? What does it look like?
5. Brief explanation of decorators
6. A look around `/custom` so we can understand how it works (I expect a lot of questions)
   1. Sockets (maybe whip up telnet): would be awesome to have a small example here too
   2. Multi-threading
   3. `Request` and `Response` objects (`HTTPException` too)
7. How can we improve this?
   1. Thread pools
   2. Handling the exit gracefully
   3. More HTTP methods
   4. Better net compliance / politeness
   5. Chunked HTTP methods (sometimes the client or server needs to split content like an image into multiple messages)

### Commands
Post Katara:
```
curl -H "Content-Type: application/json" --request POST --data '{"name": "Katara", "element": "water"}' http://localhost:8000/bender
```
Get Katara:
```
curl 'localhost:8000/bender?name=Katara'
```