main            # стабильная версия (защищена)
develop         # разработка (общая для всех)
feature/*       # фичи фронтенда/бекенда

front:
# Утром
git checkout develop
git pull origin develop
git checkout -b feature/frontend-new-component

# Работаем в client/
git add client/src/components/NewComponent.js
git commit -m "feat(frontend): add new component"

# Вечером/когда готово
git push origin feature/frontend-new-component
# Создаем Pull Request в develop


back:
git checkout develop  
git pull origin develop
git checkout -b feature/backend-new-endpoint

# Работаем в server/
git add server/routes/newEndpoint.js
git commit -m "feat(backend): add new endpoint"

git push origin feature/backend-new-endpoint
# Создаем Pull Request в develop


коммиты:
# Фронтенд
git commit -m "feat(frontend): add user profile page"
git commit -m "fix(frontend): resolve button click issue"

# Бекенд  
git commit -m "feat(backend): implement auth middleware"
git commit -m "docs(backend): update API documentation"




Мерж в мейн (релиз):
# Когда накопилось достаточно фич
git checkout main
git pull origin main
git merge develop
git push origin main

# Создаем тег версии
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin --tags




Конфликты:
# Если конфликт
git merge --abort
git checkout develop
git pull origin develop
git checkout feature/my-branch  
git rebase develop
# Решаем конфликты вручную
git rebase --continue