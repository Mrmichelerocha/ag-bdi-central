from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model
from uagents.resolver import RulesBasedResolver

class Create_agent():  

    CENTRAL_ADDRESS = "agent1qv2l7qzcd2g2rcv2p93tqflrcaq5dk7c2xc7fcnfq3s37zgkhxjmq5mfyvz"
    VISION_ADDRESS = "agent1qv73me5ql7kl30t0grehalj0aau0l4hpthp4m5q9v4qk2hz8h63vzpgyadp"
    
    resolve=RulesBasedResolver(
        {
            CENTRAL_ADDRESS: "http://127.0.0.1:8020/submit",
            VISION_ADDRESS: "http://127.0.0.1:8021/submit",
        }
    )
    
    def Agent0():
        agent0 = Agent(
            name="agent0",
            port=8020,
            seed="agent0 secret phrase",
            endpoint= ["http://127.0.0.1:8000/submit"]
            # resolve= Create_agent.resolve,
        )
        
        fund_agent_if_low(agent0.wallet.address())
        
        return agent0
    
    def Central():   
        central = Agent(
            name="central",
            port=8021,
            seed="agent1 secret phrase",
            resolve= Create_agent.resolve,
            
        )
        
        fund_agent_if_low(central.wallet.address())
        
        return central
        
    def Vision():
        vision = Agent(
            name="vision",
            port=8022,
            seed="agent2 secret phrase",
            resolve= Create_agent.resolve,
        )
        
        fund_agent_if_low(vision.wallet.address())
        
        return vision
    