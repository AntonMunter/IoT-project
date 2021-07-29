import logo from '../logo.svg';
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Header from './Header';
import "./app.scss"



const App = () =>{
  return (
    <div className="app-container">
      <Header/>

    </div>
  );
}


export default App;