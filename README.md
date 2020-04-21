# luke 路客

此为后端程序，通过 Python + Django + Django Rest Framework 提供了 RESTful APIs。

仅为学习交流目的。

## APP 构想

基于地点、话题、情绪的松散的社交应用。

- 地点：餐厅、影院、马路、城市（旅游景点），等等。
- 话题：社会事件，正在热映的电影，等等。
- 情绪：孤独，无聊，等等。

### 没有粉丝或好友

匿名，公开，平等。没有好友和粉丝的概念。
手机号或邮箱注册，昵称允许重名、更改，账号允许删除。
注册的唯一目的，是为了当用户换了设备之后还能找回以前的消息，否则可以直接随机生成一个ID，这个ID对用户透明，跟设备和系统相关，用户只要设置昵称就可以立即使用。

### 没有严格的时间线

消息没有严格的时间线。
顶得多的消息，会长期得到推送。用户也可以主动“刷新”自己发过的消息，以便得到更多推送机会。
这样可以保证那些有价值的消息，长期得到关注。

### 不喜欢就踩

一条消息，你可以“顶”，也可以“踩”。
顶得越多，消息越容易得到推送（被更多人看到）；踩得越多，消息便会沉下去。

微信和微博都只有“赞” ，而没有“不赞”或“不喜欢”。因为它们建立在“朋友”和“粉丝”的关系之上，在这种关系中，没有人希望被讨厌或批评，所以它们也比较虚假。

过客没有好友和粉丝的概念，大家互不相识，没必要忌讳，“踩”这个功能非常合适，不喜欢的消息你可以尽情的踩。

### 消息内容

一条消息必须包含一段文字，图片和小视频都是可选的，但你可以同时包含这三者。

除了这三者，消息还可以附带：

- 地址信息
- 标签（Tag）
- 情绪（表情图标）

地址在发布消息时自动生成，但是需要用户确认，用户也可以选择不加地址。这一点跟微信、微博类似。
标签系统会根据文字内容自动生成，但是会建议用户手动填写。用户在填写标签时，系统会自动补全。

地址和标签，方便了系统对消息进行归类，系统便能更精准地推送。

系统预设十来种情绪，每种情绪都由一个小图标，比如微笑、流泪、鄙视，等等。
情绪也便于系统对消息进行推送，比如心情不好的用户，尽量推送一些积极的内容。

### 讨论

任何人都可以就某个地点、话题发起讨论，讨论是临时的，二十四小时内没有人发言，系统会自动解散这个讨论。

### 私信

类似于电邮，为臭味相投的用户提供保持联系的一种方式。

## Build & Run

### Dependencies

```bash
$ pip install django djangorestframework pillow
```
`pillow` is required by Django `ImageField`.


To support OpenAPI and Swagger UI:
```bash
$ pip install pyyaml uritemplate
```

### Create PyCharm Project

Create a new project in **PyCharm** with "File / New Project...", specify the path to `mysite` as the location, e.g., `/home/adam/github/luke/mysite`.

PyCharm will ask:
> The directory '...' is not empty. Would you like to create a project from existing sources instead?

Click Yes. Follow the instructions, then your projcet should be opened in PyCharm.

### Migrate DB

`Sqlite3` is used during the development. Run `migrate.sh` to migrate the DB:
```
$ ./migrate.h
```

`migrate.sh` is no magic but the following commands:
```bash
$ rm -r luke/migrations
$ python3 manage.py makemigrations luke
$ python3 manage.py migrate
```

This will recreate DB tables (If your DB is sqlite3, there will be a file named "db.sqlite3" under current folder).
You need to do this almost whenever you change the fields of your models.

### Run

```bash
$ ./run.sh
```
Which is actually:
```
$ python3 manage.py runserver
```

Now you should be able to access `http://127.0.0.1:8000/` in your Browser.

