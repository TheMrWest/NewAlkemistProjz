# Script de doar QI Em chats.

# - Capturar o ID de um chat.
# - Utilizar esse ID para poder doar QI.

import projz
import requests
import asyncio
import csv
import os

arq_open = open(os.path.dirname(os.path.realpath(__file__)) + "/acc.txt", 'r')
csv_accounts = csv.DictReader(arq_open)

async def main(email, passw):
    client = projz.Client()
    try:
        await client.login_email(email, passw)
        print("Logado no email", email)
        return client
    
    except (projz.error.ApiException, projz.error.InvalidEmail) as err:
        print(f"Erro na conta {email} - {err}")

async def send_qi_for_account(client, chat_id):
    try:
        await client.send_qi(object_id=int(chat_id), count=10)
        print(f"QI doado pela conta:", client.account.email)
    except Exception as err:
        print(client, err)

async def get_chat_id():
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input, "Link Do chat: ")

def return_id_with_link_projz(link_id):
    return requests.post("https://www.projz.com/api/f/v1/parse-share-link", json={
        "link": link_id
    }).json()


async def run_accounts(list_accounts):
    task = []
    logged_client = {}

    for x in list_accounts:
        email = x['EMAIL'].strip()
        passw = x['PASSW'].strip()

        task.append(main(email, passw))

    r = await asyncio.gather(*task)
    for c in r:
        if c:
            logged_client[c.account.email] = c

    while True:
        print("---")
        chat_id = await get_chat_id()
        info_chat = return_id_with_link_projz(chat_id)

        if info_chat['objectType'] == 1:
            object_id = info_chat["objectId"]

            t = [send_qi_for_account(client, object_id) for client in logged_client.values()]
            await asyncio.gather(*t)

        else:
            print("Link inválido")


if __name__ == "__main__":
    print("..")
    asyncio.run(run_accounts(csv_accounts))


