// import React from 'react';
// import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';


// function App() {
//   return (
//     <Router>
//       <Switch>
//         <Route path="/" exact component={Home} />
//         <Route path="/login" component={Login} />
//         <Route path="/user-dashboard" component={UserDashboardPage} />
//         <Route path="/salesperson-dashboard" component={SalespersonDashboardPage} />
//         <Route path="/martowner-dashboard" component={MartOwnerDashboardPage} />
//       </Switch>
//     </Router>
//   );
// }

// export default App;

import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Home from './pages/Home';
import Login from './pages/Login';
import UserDashboardPage from './pages/UserDashboardPage';
import SalespersonDashboardPage from './pages/SalespersonDashboardPage';
import MartOwnerDashboardPage from './pages/MartOwnerDashboardPage';

const App = () => {
  return (
    <Router>
    
        <Routes>
        <Route path="/" exact component={Home} />
         <Route path="/login" component={Login} />      <Route path="/user-dashboard" component={UserDashboardPage} />
<Route path="/salesperson-dashboard" component={SalespersonDashboardPage} />
       <Route path="/martowner-dashboard" component={MartOwnerDashboardPage} />
        </Routes>
  
    </Router>
  );
}

export default App;