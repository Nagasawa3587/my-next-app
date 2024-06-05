import axios from 'axios';
import { useState, useEffect } from 'react';
import styled from 'styled-components';

interface Todo {
  id: number;
  number: number; // No.
  addedDate: string; // 追加日
  deadline: string; // 期限
  title: string; // タスク名
  priority: number; // 優先度（数値型） ¥ß
}

const Input = styled.input`
  padding: 8px;
  margin: 5px;
  border: 1px solid #ddd;
`;

const Select = styled.select`
  padding: 8px;
  margin: 5px;
  border: 1px solid #ddd;
`;

const Button = styled.button`
  padding: 8px 15px;
  margin: 5px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  display: inline-block;

  &:hover {
    background-color: #45a049;
  }
`;

const TodoTable = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const TodoHeader = styled.th`
  background-color: #f4f4f4;
  padding: 8px;
  border: 1px solid #ddd;
`;

const TodoRow = styled.tr`
  &:nth-child(even) {
    background-color: #f9f9f9;
  }
`;

const TodoData = styled.td`
  padding: 8px;
  border: 1px solid #ddd;
  text-align: center;
`;

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState({
    title: '',
    deadline: '',
    priority: '中'
  });

  useEffect(() => {
    axios.get('http://localhost:8000/todos/')
         .then(response => setTodos(response.data))
         .catch(error => console.error('Error fetching todos:', error));
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setNewTodo({
      ...newTodo,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const todoToAdd = {
      ...newTodo,
      addedDate: new Date().toISOString().slice(0, 10), // Set current date
      number: todos.length + 1 // Auto increment number
    };
    axios.post('http://localhost:8000/todos/', {
      due_date: new Date(newTodo.deadline),
      task_name: newTodo.title,
      priority: newTodo.priority
    })
         .then(response => {
           setTodos([...todos, response.data]);
           setNewTodo({ title: '', deadline: '', priority: '中' }); // Reset form
         })
         .catch(error => {
           console.error('Error posting todo:', error);
           alert(`Failed to add todo. Please try again. Error: ${error.response?.data?.message || error.message}`); // User feedback
         });
  };

  const handleDelete = (id: number) => {
    axios.delete(`http://localhost:8000/todos/${id}`)
         .then(() => {
           setTodos(todos.filter(todo => todo.id !== id));
         })
         .catch(error => console.error('Error deleting todo:', error));
  };

  return (
    <div>
      <h1>Todo List</h1>
      <form onSubmit={handleSubmit}>
        <Input type="text" name="title" placeholder="タスク名" value={newTodo.title} onChange={handleInputChange} />
        <Input type="date" name="deadline" value={newTodo.deadline} onChange={handleInputChange} />
        <Select name="priority" value={newTodo.priority} onChange={handleInputChange}>
          <option value="高">高</option>
          <option value="中">中</option>
          <option value="低">低</option>
        </Select>
        <Button type="submit">Add Todo</Button>
      </form>
      <TodoTable>
        <thead>
          <tr>
            <TodoHeader>No.</TodoHeader>
            <TodoHeader>追加日</TodoHeader>
            <TodoHeader>期限</TodoHeader>
            <TodoHeader>タスク名</TodoHeader>
            <TodoHeader>優先度</TodoHeader>
            <TodoHeader>操作</TodoHeader>
          </tr>
        </thead>
        <tbody>
          {todos.map(todo => (
            <TodoRow key={todo.id}>
              <TodoData>{todo.number}</TodoData>
              <TodoData>{todo.addedDate}</TodoData>
              <TodoData>{todo.deadline}</TodoData>
              <TodoData>{todo.title}</TodoData>
              <TodoData>{todo.priority}</TodoData>
              <TodoData>
                <Button onClick={() => handleDelete(todo.id)}>Delete Todo</Button>
              </TodoData>
            </TodoRow>
          ))}
        </tbody>
      </TodoTable>
    </div>
  )
}