# discord-py-bot-template
## 내장된 기능
- Cog 관리 패널
- `도움` 명령어
- 오류 처리
- 디버그 기능
- 로그 기능
## 사용전 알아둘 것
- 이 템플릿으로 봇을 만들기 전에 최소한 타입 힌트와 클래스와 비동기 정도는 알고 시작하는 것을 추천합니다.
- Cog 관리 패널이 정상적으로 동작하기 위해서는 Cog의 클래스 이름과 파일 이름은 동일해야 합니다. 단, 대문자와 소문자는 상관없습니다.  
(예: help.py, class Help(commands.Cog) (O) / test.py, class Example(commands.Cog) (X))
## 필요한 것들
- discord.py 1.3.4+
## 코드에 문제가 있나요?
자유롭게 Pull Request나 Issue를 넣어주세요.  
또는 디스코드: eunwoo1104#9600