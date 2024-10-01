## Web-service for LLM

### Description
This web service is a layer between the language model (LLM) and other user interfaces such as Telegram/Discord bots, websites and so on. 

### Quick install

1. Create `.env` file
2. Add the following environment variables:\
`MODELNAME` - name of the language model (for example, `"llama3.1"`)\
`MODEL_URL` - URL where LLM is hosted (for example, `"http://localhost:11434"`)
3. Start web-server using command: `uvicorn main:app`
