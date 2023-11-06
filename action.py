# AÇÔES DISPONÍVEIS #
# Cada função/método corresponde a uma ação (por momento apenas simulada)
import datetime
import math
import requests
import json
import time


class Action:    
    def set_plan_hardware(self, ctx, nameKey, ctxKey, planKey):
        print(f"plano enviado ao periférico {nameKey}, {ctxKey}, {planKey}")
        esp8266_url = f"http://192.168.0.101/setplan"
    
        data = {
            "nameKey": nameKey,
            "ctxKey": json.dumps(ctxKey),
            "planKey": json.dumps(planKey)
        }

        response = requests.post(esp8266_url, data=data)

        if response.status_code == 200:
            print("POST request enviado com sucesso!")
            ctx.storage.set_belief("set_plan", "ok")
            print("###> Plan enviado <### ")
        else:
            print(f"Erro ao enviar o POST request. Código de status: {response.status_code}")      
            
    def set_belief_hardware(self, ctx, beliefsKey, valueKey):
        print(f"crença enviada ao periférico {beliefsKey}, {valueKey}")
        esp8266_url = f"http://192.168.0.101/setbeliefs"
    
        data = {
            "beliefsKey": beliefsKey,
            "beliefsValue": valueKey
        }

        response = requests.post(esp8266_url, data=data)

        if response.status_code == 200:
            print("POST request enviado com sucesso!")
            ctx.storage.set_belief("set_belief", "ok")
            print("###> Belief enviado <### ")
        else:
            print(f"Erro ao enviar o POST request. Código de status: {response.status_code}")

    def set_desire_hardware(self, ctx, desireKey):
        print(f"desejo enviado ao periférico {desireKey}")
        esp8266_url = f"http://192.168.0.101/setdesire"
        
        data = {
            "desireKey": desireKey
        }
        
        response = requests.post(esp8266_url, data=data)
        
        if response.status_code == 200:
            print("POST request enviado com sucesso!")
            ctx.storage.set_belief("set_desire", "ok")
            print("###> Desire enviado <### ")
        else:
            print(f"Erro ao enviar o POST request. Código de status: {response.status_code}")
        
    def check_memory(self, ctx):
            urls = [
                'http://localhost:8000/robot/',
                'http://localhost:8000/goal/',
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
                            if elemento['_class'] == 'robot':
                                ctx.storage.set_belief("robotx",  float(elemento['_y']))
                                ctx.storage.set_belief("roboty",  float(elemento['_x']))
                            elif elemento['_class'] == 'goal':                   
                                ctx.storage.set_belief("goalx",  float(elemento['_x']))                    
                                ctx.storage.set_belief("goaly", float(elemento['_y']))                    
                            else:
                                print("A resposta não é uma lista ou está vazia.")
                else:
                    print("Erro ao fazer a requisição GET. Código de status:", response.status_code)     
        
    def check_goal(self, ctx):
        goal_x = ctx.storage.get_belief("goalx")
        robot_x = ctx.storage.get_belief("robotx")
        
        goal_y = ctx.storage.get_belief("goaly")
        robot_y = ctx.storage.get_belief("roboty")
        
        plan_robot = []
        # Primeiro, o robô se move no eixo x
        if robot_x < goal_x:
            plan_robot.append("Right")
            while robot_x < goal_x:
                plan_robot.append("Front")
                robot_x += 1
                ctx.storage.set_belief("robotx", robot_x)

        # Em seguida, o robô se move no eixo y
        if robot_y < goal_y:
            plan_robot.append("Left")
            while robot_y < goal_y:
                plan_robot.append("Front")
                robot_y += 1
                ctx.storage.set_belief("roboty", robot_y)

        # Exibe o plano de movimento
        print(f"Plano de movimento: {plan_robot}")
        # Crie um novo dicionário com os valores invertidos
        inverted_plan = plan_robot[::-1]

        # Exiba o novo dicionário
        print(f"Plano de movimento invertido: {inverted_plan}")
        
        return inverted_plan

    def check_winning(self, ctx):
        goal_x = ctx.storage.get_belief("goalx")
        robot_x = ctx.storage.get_belief("robotx")
        
        goal_y = ctx.storage.get_belief("goaly")
        robot_y = ctx.storage.get_belief("roboty")
        
        if goal_x == robot_x and goal_y == robot_y:
            ctx.storage.set_belief("winning", True)
            self.post_memory(ctx, robot_x, robot_y)
        else:
            ctx.storage.set_belief("winning", False)
            
    def post_memory(self, ctx, robot_x, robot_y):
        url = 'http://localhost:8000/robot/'

        data = {
            "_class": "robot",
            "_x": robot_x,
            "_y": robot_y
        }

        response = requests.post(url, json=data)

        if response.status_code == 201:
            print("Solicitação POST bem-sucedida!")
        else:
            print(f"A solicitação POST falhou com o código de status: {response.status_code}")
            print(response.text)
