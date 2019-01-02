# data.go.kr-crawling
건강정보, 의약품 크롤링
ckend dir

### branch architecture

- master
  - development
      - local : feature

      - feature branch

      ```
      $ git checkout -b myfeature(feat_[issue-number]) development

      $ git commit -m "close #1 - make some function" 이슈 닫아줌

      $ git checkout devleopment
      $ git merge --no-ff myfeature 필히 머지커밋 만들어줌
      $ git branch -d myfeature
      4 git push origin development

      ```

      - development -> master 

      ```
      commit

      development branch 는 커밋 rebase , squash 하지 않고 git push
      master에는 pull request 를 통해 squash 로 머지 

      tagging

      $ git tag -a [version-number]
      $ git push origin [version-number]


      delete

      $ git branch -d feat_[issue-number]
      ```

      > https://nvie.com/posts/a-successful-git-branching-model/

      

