import axios from 'axios';
import { useState, useEffect } from 'react';
import styled from 'styled-components';

interface Todo {
  id: number;
  number: number;
  added_date: string;
  deadline: string;
  title: string;
  priority: number;
}

const Input = styled.input`
  padding: 10px; 
  margin: 10px; 
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
  border: 1px solid black; 
  cursor: pointer; 
  display: inline-block; 

  &:hover {
    background-color: #45a049;
  }
`;

const TodoTable = styled.table`
  width: 50%; 
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
    priority: 0 
  });

  useEffect(() => {
    console.log('Fetching todos...');
    axios.get('http://localhost:8000/todos/')
      .then(response => {
        console.log('Fetched Todos:', response.data);
        setTodos(response.data);
      })
      .catch(error => console.error('Error fetching todos:', error));
  }, []); // 空の依存配列を使用して、初回レンダリング時にのみ実行

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    const isNumeric = name === 'priority';
    setNewTodo({
      ...newTodo,
      [name]: isNumeric ? Number(value) : value
    });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault(); // フォームの送信を防ぐ
    const todoToAdd = {
      ...newTodo,
      added_date: new Date().toISOString().slice(0, 10),
      number: todos.length + 1
    };

    console.log('Adding todo:', todoToAdd);

    axios.post('http://localhost:8000/todos/', {
      deadline: todoToAdd.deadline,
      title: todoToAdd.title,
      priority: todoToAdd.priority
    })
      .then(response => {
        console.log('Added Todo:', response.data);
        setTodos([...todos, { 
          id: response.data.id,
          number: todoToAdd.number,
          added_date: todoToAdd.added_date,
          deadline: todoToAdd.deadline,
          title: todoToAdd.title,
          priority: todoToAdd.priority,
        }]);
        setNewTodo({ title: '', deadline: '', priority: 0 }); // フォームをリセット
      })
      .catch(error => {
        console.error('Error posting todo:', error);
        alert(`Failed to add todo. Please try again. Error: ${error.response?.data?.message || error.message}`);
      });
  };

  const handleDelete = (id: number) => {
    console.log('Deleting todo with id:', id);
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
          <option value={0}>高</option>
          <option value={1}>中</option>
          <option value={2}>低</option>
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
              <TodoData>{todo.added_date}</TodoData>
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
  );
}