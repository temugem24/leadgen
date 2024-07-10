import threading
from app.initialization import run_scheduler
from app.database import Base, engine
from app import messages
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True  # Daemon threads exit when the main program exits
scheduler_thread.start()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(messages.router)


@app.get("/")
def home():
    return {"messages": "howdy there partner"}








# @app.route('/whatsapp', methods=['POST'])
# def whatsapp():
#     message = request.values.get('Body', '').strip()
#     phone_number = request.values.get('From', '').strip()
#     print("Received message:", "'",message,"'", "from:", phone_number)
#     store_message(phone_number, message, 'incoming')
#     recent_messages = [ 
#         {
#             'id': conv.id,
#             'phone_number': conv.phone_number,
#             'message': conv.message,
#             'direction': conv.direction,
#             'timestamp': conv.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # format datetime as string
#         }
#         for conv in Conversation.query.filter_by(phone_number=phone_number).order_by(Conversation.timestamp.desc()).limit(5).all()
#     ]

#     thread = openai_client.beta.threads.create()
#     openai_client.beta.threads.messages.create(thread_id=thread.id, role="user", content=json.dumps(recent_messages))
#     run = openai_client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant.id)
#     print("Run started with the Assistant.")

#     timeout = 30  
#     start_time = time.time()
#     tool_outputs = [] 
#     assistant_response = None  

#     while time.time() - start_time < timeout:
#         run_status = openai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
      
#         if run_status.status in ['completed']:
#             time.sleep(1)  
#             messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
#             if messages.data:
#                 assistant_response = messages.data[0].content[0].text.value
#                 print(f"Assistant's response: {assistant_response}") 
#                 store_message(phone_number, assistant_response, 'outgoing')
#             break
          
#         elif run_status.status == 'requires_action' and hasattr(run_status.required_action, 'submit_tool_outputs'):
#             required_tool_calls = run_status.required_action.submit_tool_outputs.tool_calls
#             for tool_call in required_tool_calls:
#                 print(f"Processing tool call with ID: {tool_call.id}, Function Name: {tool_call.function.name}")
#                 arguments = json.loads(tool_call.function.arguments)

#                 if tool_call.function.name == "create_calendar_event":
#                     try:
#                         output = assistant.create_calendar_event(arguments["name"], arguments["datetime_str"], arguments["details"])
#                         tool_outputs.append({
#                             "tool_call_id": tool_call.id,
#                             "output": json.dumps(output)
#                         })
#                     except Exception as e:
#                         print(f"Error during 'create_calendar_event': {e}")
#                 else:
#                     print("Encountered unknown tool call function name.")
#                 time.sleep(1)

#             openai_client.beta.threads.runs.submit_tool_outputs(
#                 thread_id=thread.id,
#                 run_id=run.id,
#                 tool_outputs=tool_outputs
#             )
#             break
        

#     resp = MessagingResponse()
#     if assistant_response:
#         assistant_resp_msg = resp.message(assistant_response)
#     else:
#         assistant_resp_msg = resp.message("Thank you, your appointment has been booked.")
#     return str(resp)


# if __name__ == '__main__':
#   with app.app_context():
#     send_init_messages()
