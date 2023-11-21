import factory
import factory.fuzzy

from backend.src.database.models import Task, TaskStatus


class TaskFactory(factory.Factory):
    class Meta:
        model = Task

    title = factory.Faker("text")
    description = factory.Faker("text")
    state = factory.fuzzy.FuzzyChoice(TaskStatus)
    user_id = 1


def test_create_todo(client, token):
    response = client.post(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test todo",
            "description": "Test todo description",
            "state": "draft",
        },
    )

    assert response.json() == {
        "id": 1,
        "title": "Test todo",
        "description": "Test todo description",
        "state": "draft",
    }


def test_list_tasks(session, client, user, token):
    session.bulk_save_objects(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()["tasks"]) == 5


def test_list_tasks_pagination(session, user, client, token):
    session.bulk_save_objects(TaskFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        "/tasks/?offset=1&limit=2",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["tasks"]) == 2


def test_list_tasks_filter_title(session, user, client, token):
    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, title="Test todo 1")
    )
    session.commit()

    response = client.get(
        "/tasks/?title=Test todo 1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["tasks"]) == 5


def test_list_tasks_filter_description(session, user, client, token):
    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, description="description")
    )
    session.commit()

    response = client.get(
        "/tasks/?description=desc",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["tasks"]) == 5


def test_list_tasks_filter_state(session, user, client, token):
    session.bulk_save_objects(
        TaskFactory.create_batch(5, user_id=user.id, state=TaskStatus.draft)
    )
    session.commit()

    response = client.get(
        "/tasks/?state=draft",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["tasks"]) == 5


def test_list_tasks_filter_combined(session, user, client, token):
    session.bulk_save_objects(
        TaskFactory.create_batch(
            5,
            user_id=user.id,
            title="Test todo combined",
            description="combined description",
            state=TaskStatus.done,
        )
    )

    session.bulk_save_objects(
        TaskFactory.create_batch(
            3,
            user_id=user.id,
            title="Other title",
            description="other description",
            state=TaskStatus.todo,
        )
    )
    session.commit()

    response = client.get(
        "/tasks/?title=Test todo combined&description=combined&state=done",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert len(response.json()["tasks"]) == 5


def test_update_task(session, client, user, token):
    task = TaskFactory(user_id=user.id)

    session.add(task)
    session.commit()

    response = client.put(
        f"/tasks/{task.id}",
        json={"title": "teste!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "teste!"


def test_update_inexistent_task(client, token):
    response = client.put(
        "/tasks/10",
        json={"title": "teste!"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Task não encontrada"}


def test_update_task_with_wrong_user(session, client, token, other_user):
    task = TaskFactory(user_id=other_user.id)

    session.add(task)
    session.commit()

    response = client.put(
        f"/tasks/{task.id}",
        json={"title": "teste!"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Sem permissão."}


def test_delete_todo(session, client, user, token):
    todo = TaskFactory(id=1, user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(
        f"/tasks/{todo.id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json() == {"msg": "Task deletada."}


def test_delete_todo_error(client, token):
    response = client.delete(
        f"/tasks/{10}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Task não encontrada"}
