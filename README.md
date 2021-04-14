# korean-wikipedia-corpus

<a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/3.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/3.0/">Creative Commons Attribution-ShareAlike 3.0 Unported License</a>.

한국어 위키피디아 코퍼스

## 텍스트 추출 방법

wikiextractor를 통해 한번 뽑아낸 다음, `<doc>`안의 문장들을 전부 개행문자로 이어붙여 놓았습니다. 문서와 문서 사이에는 개행문자 두개가 존재합니다. 위키피디아의 텍스트 특성상 `다. `(띄어쓰기 포함)으로 분절하면 문장이 유효하게 분절될 것이라 생각해 해당 방법대로 문장을 전부 나누어 놓았습니다. 또한 문서 자체가 100자 미만일 경우 해당 문서는 저장하지 않습니다.

즉, 아래와 같은 포맷입니다.

```text
문서1 - 문장1
문서1 - 문장2
문서1 - 문장...
문서1 - 문장n

문서2 - 문장1
문서2 - 문장2
문서2 - 문장...
문서2 - 문장m

문서3 - 문장1
문서3 - 문장2
문서3 - 문장...
문서3 - 문장m

...
```

## 사용법

1. <https://ko.wikipedia.org/wiki/위키백과:데이터베이스_다운로드>에서 덤프파일 다운로드
2. 텍스트 파일로 변환

    ```sh
    docker run \
        --rm \
        -it \
        -w /app \
        -v `pwd`:/app \
        -v WIKI_FILE_PATH:/wiki.xml.bz2:ro \
        -e WIKI_FILE=/wiki.xml.bz2 \
        python:3.6 bash -c ./extract-text.sh
    ```

    이 단계 후에도 문서 제목과 `<doc></doc>` 태그가 남아있어 아래 스크립트를 추가했습니다.

3. 텍스트만 추출

    ```sh
    docker run \
        --rm \
        -it \
        -w /app \
        -v `pwd`:/app \
        python:3.6 bash -c ./preprocess-text.sh
    ```
