# AÇÔES DISPONÍVEIS #
# Cada função/método corresponde a uma ação (por momento apenas simulada)
import datetime
import math
import requests
import json
import time


class Action:    
    def set_plan_hardware(self, ctx, nameKey, ctxKey, planKey):
        print("setei o plano")
        # esp8266_url = f"http://192.168.161.84/setplan"
    
        # data = {
        #     "nameKey": nameKey,
        #     "ctxKey": json.dumps(ctxKey),
        #     "planKey": json.dumps(planKey)
        # }

        # response = requests.post(esp8266_url, data=data)

        # if response.status_code == 200:
        #     print("POST request enviado com sucesso!")
        #     ctx.storage.set_belief("set_plan", "ok")
        #     print("###> Plan enviado <### ")
        # else:
        #     print(f"Erro ao enviar o POST request. Código de status: {response.status_code}")      
            
    def set_belief_hardware(self, ctx, beliefsKey, beliefsValue):
        print("setei as crenças")
        # esp8266_url = f"http://192.168.161.84/setbeliefs"
    
        # data = {
        #     "beliefsKey": beliefsKey,
        #     "beliefsValue": beliefsValue
        # }

        # response = requests.post(esp8266_url, data=data)

        # if response.status_code == 200:
        #     print("POST request enviado com sucesso!")
        #     ctx.storage.set_belief("set_belief", "ok")
        #     print("###> Belief enviado <### ")
        # else:
        #     print(f"Erro ao enviar o POST request. Código de status: {response.status_code}")

    def set_desire_hardware(self, ctx, desireKey):
        print("setei a desire (move ou outras)")
        # esp8266_url = f"http://192.168.161.84/setdesire"
        
        # data = {
        #     "desireKey": desireKey
        # }
        
        # response = requests.post(esp8266_url, data=data)
        
        # if response.status_code == 200:
        #     print("POST request enviado com sucesso!")
        #     ctx.storage.set_belief("set_desire", "ok")
        #     print("###> Desire enviado <### ")
        # else:
        #     print(f"Erro ao enviar o POST request. Código de status: {response.status_code}")
        
    def date(self, ctx):
        time = datetime.datetime.now().strftime('%H:%M')
        ctx.storage.set_belief("horary", time)
        print("###> update horary <###")
        
    def check_memory(self, ctx):
            urls = [
                'http://localhost:8000/obstacle/',
                'http://localhost:8000/robot/',
                'http://localhost:8000/goal/'
            ]

            for url in urls:
                response = requests.get(url)

                print(f"Verificando URL: {url}")

                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0:
                        elemento = data[-1]
                        print("Requisição GET bem-sucedida!")
                        print("Último elemento:")
                        print(elemento)
                        if '_class' in elemento:
                            if elemento['_class'] == 'obstaculo':
                                ctx.storage.set_belief("obstacle", True)
                                ctx.storage.set_belief("obstaclex", float(elemento['_x']))
                                ctx.storage.set_belief("obstacley", float(elemento['_y']))
                            elif elemento['_class'] == 'robo 1':
                                ctx.storage.set_belief("robot1y",  float(elemento['_x']))
                                ctx.storage.set_belief("robot1x",  float(elemento['_y']))
                            elif elemento['_class'] == 'robo 2':
                                ctx.storage.set_belief("robot2x",  float(elemento['_x']))
                                ctx.storage.set_belief("robot2y", float(elemento['_y']))
                            elif elemento['_class'] == 'objetivo':                   
                                ctx.storage.set_belief("goalx",  float(elemento['_x']))                    
                                ctx.storage.set_belief("goaly", float(elemento['_y']))                    
                            else:
                                print("A resposta não é uma lista ou está vazia.")
                else:
                    print("Erro ao fazer a requisição GET. Código de status:", response.status_code)     

    def check_robot(self, ctx):
        bb = ctx.storage.all_belief()
        
        if 'robot 2' in bb:
            ctx.storage.set_belief("vision_robot2", True)
        else:
            ctx.storage.set_belief("vision_robot2", False)
            
        if 'robot 1' in bb:
            ctx.storage.set_belief("vision_robot1", True)
        else:
            ctx.storage.set_belief("vision_robot1", False)
                      
    def check_obstacle(self, ctx):
        obstacle = ctx.storage.get_belief('obstacle')
        robot = ctx.storage.get_belief('robot')
        
        if obstacle and robot:
            obstacle_x = obstacle['x']
            obstacle_y = obstacle['y']
            robot_x = robot['x']
            robot_y = robot['y']
            
            # Calcula a distância euclidiana entre o robô e o obstáculo
            distance = math.sqrt((robot_x - obstacle_x)**2 + (robot_y - obstacle_y)**2)
            
            # Define um limite para considerar se o robô está perto do obstáculo
            limite_distancia = 50.0  # Ajuste esse valor conforme necessário
            
            if distance < limite_distancia:
                ctx.storage.set_belief("obstacle_ahead", True)
                print("O robô está perto do obstáculo!")
                
            else:
                ctx.storage.set_belief("obstacle_ahead", False)
                print("O robô não está perto do obstáculo.")
            
    def nearby_obstacle(self, ctx):
        self.set_desire_hardware(ctx, "mr_on")
        time.sleep(2)
        self.set_desire_hardware(ctx, "mf_on")
        time.sleep(2)
        self.set_desire_hardware(ctx, "ml_on")
        time.sleep(2)
        self.set_desire_hardware(ctx, "mf_on")
        time.sleep(2)
        self.set_desire_hardware(ctx, "ml_on")
        time.sleep(2)
        self.set_desire_hardware(ctx, "mf_on")
        time.sleep(2)
        self.set_desire_hardware(ctx, "mr_on")    
        time.sleep(2)
        
    def nearby_goal(self, ctx):
        goalx = ctx.storage.get_belief("goalx")
        goaly = ctx.storage.get_belief("goaly")
        robotx = ctx.storage.get_belief("robot1x")
        roboty = ctx.storage.get_belief("robot1y")
        
        # Calcular a diferença entre as coordenadas x e y
        dx = goalx - robotx
        dy = goaly - roboty

        # Se o robô estiver longe do objetivo em x, vire na direção certa
        if abs(dx) <= 0.1 and abs(dy) <= 0.1:  # Ajuste a tolerância conforme necessário
            # O robô chegou ao objetivo, imprima "Parabéns!".
            ctx.storage.set_belief("vision_goal", False)
            print("Parabéns!")
        else:
            # Ajusta a direção do robô com base na diferença em x e y.
            if abs(dx) > 0.1:
                # Ajuste a direção em x
                if dx > 0:
                    # Vire para a direita
                    ctx.storage.set_belief("move_front", False)
                    ctx.storage.set_belief("move_left", False)
                    ctx.storage.set_belief("move_right", True)
                else:
                    # Vire para a esquerda
                    ctx.storage.set_belief("move_front", False)
                    ctx.storage.set_belief("move_left", True)
                    ctx.storage.set_belief("move_right", False)
            else:
                # Se o robô estiver no objetivo em x, ajuste a direção em y e vá para frente.
                if dy > 0:
                    ctx.storage.set_belief("move_front", True)
                    ctx.storage.set_belief("move_left", False)
                    ctx.storage.set_belief("move_right", False)
                else:
                    ctx.storage.set_belief("move_front", True)
                    ctx.storage.set_belief("move_left", False)
                    ctx.storage.set_belief("move_right", False)