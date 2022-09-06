import time

from gevent import monkey

monkey.patch_all()

from typing import Tuple, Any

import gevent
import requests
import random

# 代理池修改
proxies = [{
    "https": "http://118.244.206.237:30201"
}]


def get_steam_data(id: int) -> Tuple[int, Any]:
    try:

        url = 'https://store.steampowered.com/apphoverpublic/' + str(id)
        # 使用代理的话 放开下面请求
        proxy = random.choice(proxies)
        resp = requests.get(url, timeout=500, proxies=proxy)
        if resp.status_code != 200:
            return id, resp
        return id, resp
    except Exception as e:
        print('异常：' + str(e))
        return id, None


def save_html(id: int):
    id, resp = get_steam_data(id)
    if len(resp.content) == 0:
        return
    f = open('./game_file/' + str(id) + '.html', 'wb')
    f.write(resp.content)
    return id


if __name__ == '__main__':

    # 循环8000次 调整
    allIds = []
    for i in range(80000):
        print('第' + str(i + 1) + '批次开始>>>>>>>>>>>')
        ids = []
        # 调整每批次数量
        for j in range(1000000 + i * 10, 1000000 + (i + 1) * 10):
            ids.append(j)
        print('待查询ID详情：' + str(1000000 + i * 10) + ' 到：' + str(1000000 + (i + 1) * 10))

        coros = [gevent.spawn(save_html, id) for id in ids]
        gevent.joinall(coros)
        for coro in coros:
            id = coro.get()
            if id:
                allIds.append(id)

        print('第' + str(i + 1) + '批次结束<<<<<<<<<<<')
        # 调整每批次间隔
        time.sleep(2)

    print('所有游戏ID列表：' + str(allIds))
