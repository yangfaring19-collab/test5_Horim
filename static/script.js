$(document).ready(function () {

    // -----------------------------
    // 1. 초기 로딩 (GET)
    // -----------------------------
    loadTodos();


    function loadTodos() {
        $.ajax({
            url: "/todos",
            type: "GET",
            success: function (res) {
                renderTodos(res);
            },
            error: function () {
                alert("할 일 목록을 불러오지 못했습니다.");
            }
        });
    }


    // -----------------------------
    // 2. 목록 렌더링
    // -----------------------------
    function renderTodos(todos) {
        const list = $("#todo-list");
        list.empty();

        todos.forEach(todo => {

            const item = `
                <li class="todo-item" data-id="${todo.id}">
                    <span class="todo-text ${todo.completed ? 'completed' : ''}">
                        ${todo.title}
                    </span>
                    <input type="text" class="edit-input hidden">

                    <div class="todo-buttons">
                        <button class="edit-btn">수정</button>
                        <button class="save-btn hidden">저장</button>
                        <button class="complete-btn">
                            ${todo.completed ? "취소" : "완료"}
                        </button>
                        <button class="delete-btn">삭제</button>
                    </div>
                </li>
            `;

            list.append(item);
        });
    }


    // -----------------------------
    // 3. 추가 (POST)
    // -----------------------------
    $("#add-btn").click(function () {

        const title = $("#todo-title").val();
        title.trim()
        if (!title) {
            alert("할 일을 입력하세요");
            return;
        }

        $.ajax({
            url: "/todos",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                title: title
            }),
            success: function () {
                $("#todo-title").val("");
                loadTodos();
            },
            error: function () {
                alert("추가 실패");
            }
        });

    });
    // -----------------------------
    // 4. 수정 (PUT)
    // -----------------------------
    $(document).on("click", ".edit-btn", function () {

        const item = $(this).closest(".todo-item");
        const text = item.find(".todo-text").text().trim();

        // input에 기존 값 넣기
        item.find(".edit-input").val(text);

        // UI 전환
        item.find(".todo-text").hide();
        item.find(".edit-input").show();

        item.find(".edit-btn").hide();
        item.find(".save-btn").show();
    });

    $(document).on("click", ".save-btn", function () {

        const item = $(this).closest(".todo-item");
        const id = item.data("id");
        const newTitle = item.find(".edit-input").val();

        if (!newTitle) {
            alert("내용을 입력하세요");
            return;
        }

        $.ajax({
            url: `/todos/${id}`,
            type: "PUT",
            contentType: "application/json",
            data: JSON.stringify({
                title: newTitle
            }),
            success: function () {
                loadTodos(); // 전체 새로고침
            },
            error: function () {
                alert("수정 실패");
            }
        });
    });


    // -----------------------------
    // 5. 완료 / 취소 (PUT)
    // -----------------------------
    $(document).on("click", ".complete-btn", function () {

        const item = $(this).closest(".todo-item");
        const id = item.data("id");

        // 현재 상태 판별 (UI 기준)
        const isCompleted = item.find(".todo-text").hasClass("completed");

        $.ajax({
            url: `/todos/${id}`,
            type: "PUT",
            contentType: "application/json",
            data: JSON.stringify({
                completed: isCompleted ? 0 : 1
            }),
            success: function () {
                loadTodos(); // 다시 렌더링
            },
            error: function () {
                alert("완료 상태 변경 실패");
            }
        });

    });


    // -----------------------------
    // 6. 삭제 (DELETE)
    // -----------------------------
    $(document).on("click", ".delete-btn", function () {

        const id = $(this).closest(".todo-item").data("id");

        $.ajax({
            url: `/todos/${id}`,
            type: "DELETE",
            success: function () {
                loadTodos();
            },
            error: function () {
                alert("삭제 실패");
            }
        });

    });

});