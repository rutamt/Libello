// With reference to https://www.youtube.com/watch?v=Efo7nIUF2JY

export default class Todo {    
    constructor(root) {

        const newTodo = document.createElement("div")
        newTodo.className = "todo__container col-lg-4 col-md-6 col-sm-12"
        newTodo.innerHTML = Todo.getHTML()

        root.appendChild(newTodo)

        this.el = {
            container: root.querySelector(".todo__container"),
            addTodobutton: root.querySelector(".btn__add-todo"),
            todoList: root.querySelector(".todo__wrapper"),
        }

        this.el.addTodobutton.addEventListener('click', () => {
            const textContent = prompt("Enter Task:")

            if (textContent === null || textContent === "") {
                console.log("Type words you bumbling idiot")
            } else {
                this.addTodo(textContent)
            }
        })

        this.getTodos().forEach((task) => {
            const taskElement = this.createTodo(task.id, task.content, task.done)
            this.el.todoList.appendChild(taskElement)
        })
    }

    getTodos() { // Get stuff from storeage
        return JSON.parse(localStorage.getItem("todolist-todos") || "[]");
    }

    saveTodos(todos) { // Save stuff into storage
        localStorage.setItem("todolist-todos", JSON.stringify(todos));
    }

    createTodo(id, content, done) { // Create the todo element
        const element = document.createElement("div");

        element.classList.add("todo");
        element.value = content;
        element.innerHTML = content;
        element.done = done;

        if (element.done) {
            element.classList.add("todo--done")
        } else {
            element.classList.remove("todo--done")
        }

        element.addEventListener("dblclick", () => {
            const newContent = prompt("Update your task (if this is left blank the note will delete):")

            if (newContent === "") {
                const doDelete = confirm("Do you want to delete this task?")

                if (doDelete) {
                    this.deleteTodo(id, element);
                }
            } else {
                this.updateTodo(id, newContent, element)
            }
        });

        element.addEventListener("click", () => {
            element.done = !element.done
            element.classList.toggle("todo--done")

            this.updateTodo(id, content, element, element.done)
        })

        return element;
    }

    addTodo(content) {
        const todos = this.getTodos();
        const todoObject = {
            id: Math.floor(Math.random() * 100000),
            content: content,
            done: false
        }

        const todoElement = this.createTodo(todoObject.id, todoObject.content, todoObject.done)
        this.el.todoList.appendChild(todoElement)

        todos.push(todoObject)
        this.saveTodos(todos)
    }

    deleteTodo(id, element) {
        const todos = this.getTodos().filter(todo => todo.id != id);

        this.saveTodos(todos)
        this.el.todoList.removeChild(element);
    }

    updateTodo(id, newContent, element, done) {
        
        const todos = this.getTodos()
        const targetTodo = todos.filter(todo => todo.id == id)[0];

        targetTodo.content = newContent;
        targetTodo.done = done;
        this.saveTodos(todos);

        element.innerHTML = newContent;

    }

    static getHTML() {
        return `
            <div class="todo__header">
                <h3 class="header-text">Todo Module</h3>
                <button class="btn__add-todo">
                    <span class="material-symbols-outlined">add</span>
                </button>
            </div>

            <div class="todo__wrapper"></div>
        `
    }
}

// Modal Boxes for error