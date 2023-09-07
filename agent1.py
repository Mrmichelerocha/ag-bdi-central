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
    central.belief(ctx, "vision_goal", True)
    central.belief(ctx, "obstacle_ahead", False)
    action.set_belief_hardware(ctx, 'Front', 'OK')
    action.set_belief_hardware(ctx, 'Right', 'OK')
    action.set_belief_hardware(ctx, 'Left', 'OK')
    action.set_plan_hardware(ctx, "mf_on", {'Front': 'OK'}, ['Front'])
    action.set_plan_hardware(ctx, "mr_on", {'Right': 'OK'}, ['Right'])
    action.set_plan_hardware(ctx, "ml_on", {'Left': 'OK'}, ['Left'])
    
    
@central.on_interval(period=5)
async def plan_interval(ctx: Context):
    action.check_memory(ctx)
    action.check_obstacle(ctx)
    action.nearby_obstacle(ctx) if central.contexto(ctx, {"obstacle_ahead": True}) else False
    action.nearby_goal(ctx) if central.contexto(ctx, {"vision_goal": True}) else False
    action.set_desire_hardware(ctx, "mf_on") if central.contexto(ctx, {"move_front": True}) else False
    action.set_desire_hardware(ctx, "ml_on") if central.contexto(ctx, {"move_left": True}) else False
    action.set_desire_hardware(ctx, "mr_on") if central.contexto(ctx, {"move_right": True}) else False

   
@central.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    pass
   
if __name__ == "__main__":
    central.run()
