from uAgents.src.uagents import Agent, Context, Model
from aumanaque import Create_agent
from action import Action
import time

class Message(Model):
    message: str
    
central = Create_agent.Central()
action = Action()
  
@central.on_event('startup')
async def plan_event(ctx: Context):
    central.belief(ctx, "goalx", 0)
    central.belief(ctx, "robotx", 0)
    central.belief(ctx, "goaly", 0)
    central.belief(ctx, "roboty", 0)
    central.belief(ctx, "winning", False)
    action.set_belief_hardware(ctx, 'Goal', 'OK')
 
@central.on_interval(period=5)
async def plan_interval(ctx: Context):
    action.check_memory(ctx)
    plan_robot = action.check_goal(ctx)
    action.set_plan_hardware(ctx, "plan_move", {"Goal": "OK"}, plan_robot) if central.contexto(ctx, {"winning": False}) else False
    action.set_desire_hardware(ctx, "plan_move") if central.contexto(ctx, {"winning": False}) else False
    action.check_winning(ctx)
   
@central.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    pass
   
if __name__ == "__main__":
    central.run()
