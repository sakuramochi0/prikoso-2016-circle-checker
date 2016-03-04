import re
import yaml
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.conf import settings
from pymongo.mongo_client import MongoClient

space_nums =[
    ('yuki_plus', 1),
    ('siokya', 2),
    ('MMM37', 3),
    ('iede_02', 4),
    ('COP__', 5),
    ('kiriuru', 6),
    ('teppan38', 7),
    ('coromo_saku2', 7),
    ('cafemoca19', 7),
    ('k4n6m9', 8),
    ('miyukisum', 9),
    ('ripo_day', 10),
    ('harapeco_pymr', 10),
    ('yuki8p', 11),
    ('ringosh_', 12),
    ('ISANAinUSA', 13),
    ('rikuK993', 14),
    ('puripash', 15),
    ('MyaMyaru', 16),
    ('nurumi_p', 17),
    ('EPI_prism', 17),
    ('jyojyojyo_', 18),
    ('kinta_ex', 19),
    ('418sds', 19),
    ('koshia_rl', 20),
    ('vamddkijg', 21),
    ('VegA__AnastasiA', 22),
    ('pa_sh_pr', 23),
    ('k_y_ma_', 23),
    ('popn_mitsuki', 24),
    ('rio_tarantella', 25),
    ('kk_sub', 26),
    ('kumodoriren', 27),
    ('mtk1600', 28),
    ('kirakira_tter08', 29),
    ('sakachico', 29),
    ('l0kinann', 30),
    ('an_dan_te074', 30),
    ('ANATANO_ARATANI', 31),
    ('tekkoubondo', 32),
    ('kondokodanuki', 33),
    ('naomachi1800ml', 34),
    ('houiP', 35),
    ('Fureiya14', 36),
    ('oremaka_000', 37),
    ('azuma333', 37),
    ('sasa_0416', 38),
    ('nanaox16', 39),
    ('eifonen', 40),
    ('chiharutosayaka', 41),
    ('White_0422', 42),
    ('qEouo', 43),
    ('indigohr_25', 44),
    ('shiopoko_6o6', 45),
    ('hutarun', 46),
    ('wt_prism', 1000),
    ('ino_zip', 1000),
    ('akarin1971', 1000),
]

def index(request, page='1', edit=None):
    page = int(page)
    cols = MongoClient().prikoso_2016.tweets
    users = []
    for name, num in sorted(space_nums, key=lambda x: x[1]): # numでソート
        # ページ外のユーザを除外
        if not 10 * (page - 1) <= num < 10 * page: # ex. page=2 ならば #10-19 を表示
            continue
        
        user = cols.find_one({'tweet.user.screen_name': name})
        if user:
            user = user['tweet']['user']
            if edit: # 編集するときは全件表示する
                pins = cols.find({
                    'tweet.user.screen_name': name,
                    'tweet.extended_entities': {'$exists': True},
                    'tweet.text': {'$not': re.compile(r'^RT ')},
                    'pin': {'$exists': True},
                }).sort('tweets.id')
                tweets = cols.find({
                    'tweet.user.screen_name': name,
                    'tweet.extended_entities': {'$exists': True},
                    'tweet.text': {'$not': re.compile(r'^RT ')},
                    'pin': {'$exists': False},
                }).sort('tweets.id')
                print(name, pins.count() + tweets.count())
                
            else: # 通常時はdisabaleされたものを除外する
                pins = cols.find({
                    'tweet.user.screen_name': name,
                    'tweet.extended_entities': {'$exists': True},
                    'tweet.text': {'$not': re.compile(r'^RT ')},
                    'disable': {'$exists': False},
                    'pin': {'$exists': True},
                }).sort('tweets.id')
                tweets = cols.find({
                    'tweet.user.screen_name': name,
                    'tweet.extended_entities': {'$exists': True},
                    'tweet.text': {'$not': re.compile(r'^RT ')},
                    'disable': {'$exists': False},
                    'pin': {'$exists': False},
                }).sort('tweets.id')

        if edit:
            users.append({
                'space_num': num,
                'user': user,
                'tweets_list': [pins, tweets[:30 - pins.count()]],
            })
        else: # editモードでない時は、表示ツイート数を制限する
            users.append({
                'space_num': num,
                'user': user,
                'tweets_list': [pins, tweets[:6 - pins.count()]],
            })

    return render(request, 'prikoso_2016_circle_checker/index.html', {'users': users, 'edit': edit})

def disable(request):
    id = request.POST.get('id')
    cols = MongoClient().prikoso_2016.tweets
    cols.update({'tweet.id_str': id}, {'$set': {'disable': True}})
    print('disabled:', id)
    return HttpResponse('')

def enable(request):
    id = request.POST.get('id')
    cols = MongoClient().prikoso_2016.tweets
    cols.update({'tweet.id_str': id}, {'$unset': {'disable': ''}})
    print('enabled:', id)
    return HttpResponse('')

def pin(request):
    id = request.POST.get('id')
    cols = MongoClient().prikoso_2016.tweets
    cols.update({'tweet.id_str': id}, {'$set': {'pin': True}})
    print('pinned:', id)
    return HttpResponse('')

def unpin(request):
    id = request.POST.get('id')
    cols = MongoClient().prikoso_2016.tweets
    cols.update({'tweet.id_str': id}, {'$unset': {'pin': ''}})
    print('unpinned:', id)
    return HttpResponse('')
