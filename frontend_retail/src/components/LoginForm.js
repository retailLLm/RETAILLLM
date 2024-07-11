import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function LoginForm() {
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
    role: 'user', // default role
  });
  const NuseNavigate = useNavigate();

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Add authentication logic here
    if (credentials.role === 'user') {
      NuseNavigate.push('/user-dashboard');
    } else if (credentials.role === 'salesperson') {
      NuseNavigate.push('/salesperson-dashboard');
    } else if (credentials.role === 'martowner') {
      NuseNavigate.push('/martowner-dashboard');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="username"
        value={credentials.username}
        onChange={handleChange}
        placeholder="Username"
        required
      />
      <input
        type="password"
        name="password"
        value={credentials.password}
        onChange={handleChange}
        placeholder="Password"
        required
      />
      <select name="role" value={credentials.role} onChange={handleChange}>
        <option value="user">User</option>
        <option value="salesperson">Salesperson</option>
        <option value="martowner">Mart Owner</option>
      </select>
      <button type="submit">Login</button>
    </form>
  );
}

export default LoginForm;
