import os
import pinecone
import openai
#ModuleNotFoundError: No module named 'telegram.ext'
import requests 
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import json 
# Initialize Pinecone client
pinecone.init(api_key=os.environ['PINECONE_API_KEY'], environment=os.environ['PINECONE_ENV'])
index = pinecone.Index(index_name=os.environ['PINECONE_INDEX'])

# Initialize OpenAI client
openai.api_key = os.environ['OPENAI_API_KEY']
user_contexts = []
# Define function to handle incoming messages
#           
def export(update, context):
    message_text = update.message.text
    which = message_text.split(" ")[1]
    user_contexts[which] = message_text.split(" ")[2]
    print(update.effective_chat.id[which])
# Define function to handle incoming messages
def handle_message(update, context):
    print(update)
    # Get the incoming message text
    print(update.message)
    print(update.message.entities)
    # Check if the message has a document
    if update.message.document:
        # Get the document file ID
        file_id = update.message.document.file_id
        print   (file_id)
        file_name = update.message.document.file_name
        print(file_name)
        # Download the document file
        file = context.bot.get_file(file_id)
        file.download(file_name)
        file = requests.get(file.file_path, stream=True).raw  
        with open (file_name, 'wb') as f:
            f.write(file.read())
        file = file_name
        # Get the incoming message text
        message_text = update.message.text
        print(message_text)

        # get user id
        user_id = update.effective_chat.id
        # send file to localhost
        # requests get raw

        # files = {'file': open(f'../{
        files = {'file': open(f'./{file}', 'rb')}
        r = requests.post(f'http://localhost:8080/process_file', files=files, data={"session_id": str(user_id)+"2"})
        # get response
        response = r.json()
        # get response text
        # add response text to file_text_dict
        context.bot.send_message(chat_id=update.effective_chat.id, text="keep going padawan..")
        return 
    message_text = update.message.text 
    if not "/" in message_text:
       

        embedding = embed(message_text, update.effective_chat.id)
        print(embedding)
        # Search for nearest neighbors in the Pinecone index
        results = index.query(
                namespace=str(update.effective_chat.id)+"2",
                top_k=14,
                include_values=False,
                include_metadata=True,
                vector=embedding
            )
        print(results)

        response_text = ""

        for i in range(len(results.matches)):
            result = results.matches[i]
            file_chunk_id = result.id
            score = result.score
            file_text = result.metadata["text"]
            file_string = f"###\n{file_text}\n"
            print(file_string)
            response_text += file_string
        # Get the response text from the nearest neighbor

        # Note: this is not the proper way to use the ChatGPT conversational format, but it works for now
        messages = [
            {
                "role": "system",
                "content": f"Using the context, spin the content in a conversational and educational tone as jarett dunn. the context is previous chats he's had with other people. the query is an article he's been tasked with spinning\n\n" \
                                                f"Query: {message_text}\n\n" \
                f"Context: {response_text}\n\n" \
                f"Response: "
            },
        ]

        response = openai.ChatCompletion.create(
            messages=messages,
            model='gpt-4',
            max_tokens=2000,
            temperature=0.0,
        )

        choices = response["choices"]  # type: ignore
        answer = choices[0].message.content.strip()
        # Send the response back to the user
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
# Define function to embed text using OpenAI's text-embedding-ada-002 model
def embed(text, user):
    response = openai.Embedding.create(
  model="text-embedding-ada-002",
  input=text,
  user=str(user)
)
# response data embedding
    embedding = json.loads(str(response))["data"][0]['embedding']
    return embedding



# Define function to get response text using OpenAI's GPT-4 model
def get_response(embedding_id):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=f"Generate a response based on the following embedding ID: {embedding_id}",
        max_tokens=138,
        n=1,
        stop=None,
        temperature=0.7,
    )

    response_text = response.choices[0].text.strip()
    return response_text

# Set up the Telegram bot
updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
dispatcher = updater.dispatcher
# dispatcher slash commands

dispatcher.add_handler(CommandHandler("export", export))

# Add message handler to the dispatcher
message_handler = MessageHandler(~Filters.command, handle_message)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()