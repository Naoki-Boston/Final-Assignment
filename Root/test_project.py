# test_project.py
import os
import json
import pytest
from datetime import datetime, timedelta
from project import add_task, list_tasks, complete_task, delete_task, load_tasks, save_tasks

# テスト用のタスクファイル
TEST_TASKS_FILE = "test_tasks.json"

# テスト用のオリジナルタスクファイル名を保存
original_tasks_file = None

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """各テストの前後で実行される処理"""
    # セットアップ
    global original_tasks_file
    from project import TASKS_FILE
    original_tasks_file = TASKS_FILE
    
    # テスト用のファイルを使用するようにモジュール変数を書き換え
    import project
    project.TASKS_FILE = TEST_TASKS_FILE
    
    # テスト用のデータファイルがあれば削除
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)
    
    yield  # テスト実行
    
    # クリーンアップ
    if os.path.exists(TEST_TASKS_FILE):
        os.remove(TEST_TASKS_FILE)
    
    # オリジナルのファイル名を戻す
    project.TASKS_FILE = original_tasks_file

def test_add_task():
    """add_task関数のテスト"""
    # 基本的なタスク追加のテスト
    task = add_task("テストタスク", "high", "2023-12-31")
    
    assert task["title"] == "テストタスク"
    assert task["priority"] == "high"
    assert task["due_date"] == "2023-12-31"
    assert task["completed"] == False
    assert "created_at" in task
    
    # デフォルト値のテスト
    task2 = add_task("デフォルトタスク")
    
    assert task2["title"] == "デフォルトタスク"
    assert task2["priority"] == "medium"
    assert task2["due_date"] is None
    assert task2["completed"] == False
    
    # タスクが保存されているか確認
    tasks = load_tasks()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "テストタスク"
    assert tasks[1]["title"] == "デフォルトタスク"

def test_list_tasks(capsys):
    """list_tasks関数のテスト"""
    # テスト用のタスクを追加
    add_task("高優先度タスク", "high", "2023-12-31")
    add_task("中優先度タスク", "medium", "2024-01-15")
    add_task("低優先度タスク", "low", None)
    
    # タスクの一つを完了としてマーク
    complete_task(2)
    
    # すべてのタスクを表示
    tasks = list_tasks(show_all=True)
    assert len(tasks) == 3
    
    # 完了していないタスクのみ表示
    tasks = list_tasks(show_all=False)
    assert len(tasks) == 2
    
    # 優先度でフィルタリング
    tasks = list_tasks(show_all=True, priority_filter="high")
    assert len(tasks) == 1
    assert tasks[0]["title"] == "高優先度タスク"
    
    # 出力内容の確認
    captured = capsys.readouterr()
    assert "高優先度タスク" in captured.out

def test_complete_task():
    """complete_task関数のテスト"""
    # テスト用のタスクを追加
    add_task("完了するタスク", "medium")
    
    # タスクを完了としてマーク
    result = complete_task(1)
    assert result == True
    
    # タスクが完了としてマークされているか確認
    tasks = load_tasks()
    assert tasks[0]["completed"] == True
    assert "completed_at" in tasks[0]
    
    # 存在しないタスクIDの場合
    result = complete_task(999)
    assert result == False

def test_delete_task():
    """delete_task関数のテスト"""
    # テスト用のタスクを追加
    add_task("削除するタスク1", "medium")
    add_task("削除するタスク2", "high")
    
    # タスクを削除
    result = delete_task(1)
    assert result == True
    
    # タスクが削除されているか確認
    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "削除するタスク2"
    
    # 存在しないタスクIDの場合
    result = delete_task(999)
    assert result == False

def test_load_and_save_tasks():
    """load_tasks関数とsave_tasks関数のテスト"""
    # テスト用のデータ
    test_tasks = [
        {
            "id": 1,
            "title": "テストタスク1",
            "priority": "high",
            "due_date": "2023-12-31",
            "completed": False,
            "created_at": "2023-01-01 12:00:00"
        },
        {
            "id": 2,
            "title": "テストタスク2",
            "priority": "low",
            "due_date": None,
            "completed": True,
            "created_at": "2023-01-02 12:00:00",
            "completed_at": "2023-01-03 12:00:00"
        }
    ]
    
    # タスクを保存
    save_tasks(test_tasks)
    
    # 保存したタスクを読み込み
    loaded_tasks = load_tasks()
    
    # データが一致するか確認
    assert len(loaded_tasks) == 2
    assert loaded_tasks[0]["id"] == 1
    assert loaded_tasks[0]["title"] == "テストタスク1"
    assert loaded_tasks[1]["id"] == 2
    assert loaded_tasks[1]["completed"] == True