
import chainlit as cl
from chainlit.input_widget import Select, Slider, Switch


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "apmin"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None

@cl.on_chat_resume
async def on_chat_resume(thread):
    pass


@cl.step(type="tool")
async def tool_5():
    # Fake tool
    await cl.sleep(2)
    return "Response from the tool!"


@cl.action_callback("action_button1")
async def on_action(action):
    await cl.Message(content=f"Executed {action.name}").send()
    # Optionally remove the action button from the chatbot user interface
    await action.remove()

@cl.set_chat_profiles
async def chat_profile(usr):
    print('Invoke chat profiles', usr.metadata,usr.metadata.get('email'))
    return [
        cl.ChatProfile(
            name="WS100",
            markdown_description="""Explore **Lilly file.csv**.
            """,
            icon="https://picsum.photos/200",
            starters=[
                cl.Starter(
                    label="Describe it.",
                    message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
                    icon="https://picsum.photos/200",
                    ),

                cl.Starter(
                    label="Auto-discover",
                    message="Can you help me create a personalized morning routine that would help increase my productivity throughout the day? Start by asking me about my current habits and what activities energize me in the morning.",
                    icon="https://picsum.photos/200",
                    ),

                cl.Starter(
                    label="Help",
                    message="Explain superconductors like I'm five years old.",
                    icon="https://picsum.photos/200",
                    ),
            ]
        ),
        # cl.ChatProfile(
        #     name="GPT-4",
        #     markdown_description="The underlying LLM model is **GPT-4**.",
        #     icon="https://picsum.photos/250",
        # ),
    ]


@cl.on_chat_start
async def start(*args, **kwargs):
    usr = cl.user_session.get('user')
    print('Invoke chat start', usr.metadata)
    await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="Choose between QA or SQL API",
                values=["QA", "SQL"],
                initial_index=0,
            ),

            Select(
                id="Style",
                label="Conversation Style",
                values="Normal,Concise,Explanatory,Formal".split(','),
                initial_index=0,
            ),

        ]
    ).send()

@cl.on_message  # this function will be called every time a user inputs a message in the UI
async def main(message: cl.Message):
    """
    This function is called every time a user inputs a message in the UI.
    It sends back an intermediate response from the tool, followed by the final answer.

    Args:
        message: The user's message.

    Returns:
        None.
    """


    # res = await cl.AskActionMessage(
    #     content="Pick an action!",
    #     actions=[
    #         cl.Action(name="continue", payload={"value": "continue"}, label="✅ Continue"),
    #         cl.Action(name="cancel", payload={"value": "cancel"}, label="❌ Cancel"),
    #     ],
    # ).send()

    # if res and res.get("payload").get("value") == "continue":
    #     await cl.Message(
    #         content="Continue!",
    #     ).send()




    # r = cl.Message(content="Nice")
    
    # async with cl.Step(name="Processing data very intensively ...") as step:
    #     # step.input = "Parent step input"
    #     step.output = "Parent step output AAAA"
    #     await step.update()
    #     await cl.sleep(6)
        
    #     await r.send()
    #     await cl.sleep(4)
    #     r.content = "Nice\nNice 2"
    #     await r.update()

    #     step.output = "Parent step output ----- BBBBBB"
    #     await step.update()
    #     await cl.sleep(6)
    #     await step.remove()

    # await cl.Message(content="Nice").send(); await cl.sleep(1)

    
    # df = pd.DataFrame([[1,1], [2,3]], columns=["A", "B"])
    # print(df)

    # elements = [cl.Dataframe(data=df, display="side", name="Dataframe")]

    # await cl.Message(content="This Dataframe message has a ", elements=elements).send()


    # image = 'https://picsum.photos/200/300'
    # image = cl.Image(url=image, name="image1", display="inline")

    # # Attach the image to the message
    # await cl.Message(
    #     content="This message has an image!",
    #     elements=[image],
    # ).send()


    # fig = go.Figure(
    #     data=[go.Bar(y=[2, 1, 3])],
    #     layout_title_text="An example figure",
    # )
    # elements = [cl.Plotly(name="chart", figure=fig, display="inline")]

    # await cl.Message(content="This message has a chart", elements=elements).send()
    task_list = cl.TaskList()
    task_list.status = "Running..."

    # Create a task and put it in the running state
    task1 = cl.Task(title="Processing data", status=cl.TaskStatus.RUNNING)
    await task_list.add_task(task1)
    # Create another task that is in the ready state
    task2 = cl.Task(title="Performing calculations")
    await task_list.add_task(task2)

    # Optional: link a message to each task to allow task navigation in the chat history
    message = await cl.Message(content="Started processing data").send()
    task1.forId = message.id

    # Update the task list in the interface
    await task_list.send()

    # Perform some action on your end
    await cl.sleep(1)

    # Update the task statuses
    task1.status = cl.TaskStatus.DONE
    task2.status = cl.TaskStatus.FAILED
    task_list.status = "Failed"
    await task_list.send()