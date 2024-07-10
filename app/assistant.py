import openai
import time
import json
from dotenv import load_dotenv
from app.functions import create_calendar_event
from app.config import settings

load_dotenv()

client = openai.OpenAI(api_key=settings.openai_api_key)
model = settings.model


class AssistantManager:
    assistant_id = settings.assistant_id

    def __init__(self, model: str = model):
        self.client = client
        self.model = model
        self.assistant = None
        self.run = None

        # Retrieve existing assistant and thread if IDs are already set
        if AssistantManager.assistant_id:
            self.assistant = self.client.beta.assistants.retrieve(
                assistant_id=AssistantManager.assistant_id
            )


    def create_assistant(self, name, instructions, tools):
        if not self.assistant:
            assistant_obj = self.client.beta.assistants.create(
                name=name, instructions=instructions, tools=tools, model=self.model
            )
            AssistantManager.assistant_id = assistant_obj.id
            self.assistant = assistant_obj
            print(f"AssisID:::: {self.assistant.id}")

    def create_thread(self):
        if not self.thread:
            thread_obj = self.client.beta.threads.create()
            AssistantManager.thread_id = thread_obj.id
            self.thread = thread_obj
            print(f"ThreadID::: {self.thread.id}")
            return AssistantManager.thread_id

    def add_message_to_thread(self, thread_id, role, content):
                self.client.beta.threads.messages.create(
                    thread_id=thread_id, role=role, content=content
                )

    def run_assistant(self, thread_id):
            self.run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant.id
            )

    def process_message(self, thread_id):
            messages = self.client.beta.threads.messages.list(thread_id=thread_id)

            last_message = messages.data[0]
            response = last_message.content[0].text.value

            return response
            # summary.append(response)
            # self.summary = "\n".join(summary)
            # print(f"SUMMARY-----> {role.capitalize()}: {response}")

            # for msg in messages:
            #     role = msg.role
            #     content = msg.content[0].text.value
            #     print(f"SUMMARY-----> {role.capitalize()}: ==> {content}")

    def call_required_functions(self, required_actions):
        if self.run:
            tool_outputs = []

            for action in required_actions["tool_calls"]:
                func_name = action["function"]["name"]
                arguments = json.loads(action["function"]["arguments"])

                if func_name == "create_calendar_event":
                    output = create_calendar_event(
                        name=arguments["name"], 
                        datetime_str=arguments["datetime_str"])
                    print(f"STUFFFFF;;;;{output}")
                    final_str = ""
                    for item in output:
                        final_str += "".join(item)

                    tool_outputs.append({"tool_call_id": action["id"], "output": final_str})
                else:
                    raise ValueError(f"Unknown function: {func_name}")

            print("Submitting outputs back to the Assistant...")
            self.client.beta.threads.runs.submit_tool_outputs(
                thread_id=self.thread.id, run_id=self.run.id, tool_outputs=tool_outputs
            )
    

    def wait_for_completion(self, thread_id):
        if self.run:
            while True:
                time.sleep(3)
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id, run_id=self.run.id
                )

                if run_status.status == "completed":
                    self.process_message(thread_id)
                    break
                elif run_status.status == "requires_action":
                    print("FUNCTION CALLING NOW...")
                    self.call_required_functions(
                        required_actions=run_status.required_action.submit_tool_outputs.model_dump()
                    )
                    