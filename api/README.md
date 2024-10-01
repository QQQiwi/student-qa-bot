## Web-service for LLM

### Description
This web service is a layer between the language model (LLM) and other user interfaces such as Telegram/Discord bots, websites and so on. 

### Quick install

1. Create `.env` file
2. Add the following environment variables:\
`MODELNAME` - name of the language model (for example, `"llama3.1"`)\
`MODEL_URL` - URL where LLM is hosted (for example, `"http://localhost:11434"`)
3. Start web-server using command: `uvicorn main:app`

## Endpoints

### 1. `/requests_chat`
Request to LLM with chat history and answers based on previous dialogue. Accepts JSON-body:\
```{"user_id": int, "messages": list}```.\
Field `"messages"` is a list of JSONs that contains chat history, each message's JSON format:\
```{"role": str, "content": str}```. \
Field `"role"` should be either `user` or `assistant`. Field `content` contains message text.

### 2. `/requests_generate`
Request to LLM to generate a response for a given prompt. Accepts JSON-body:\
```{"user_id": int, "prompt": str}```\
Field `"prompt"` contains prompt to LLM as a string.

## Response models
Response model:
`{"message": str, "done": bool}`

The response models are completely identical except for the first field:  
`"message"` for `/request_chat` \
and `"response"` for `/request_generate`