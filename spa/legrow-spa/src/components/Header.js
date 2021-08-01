import logo from '../logo.svg';
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import Home from "./Home";
import Temp from "./Temp";
import Moist from "./Moist";
import "./header.scss"



const Header = () =>{
  return (
    <HashRouter>
        <header className='header'>
            <div className='logo'>
              <h1>LeGrow</h1>
            </div>
            <nav>
              <ul>
                <li><NavLink to="/" exact={true}><div className='btn'><span>Home</span></div></NavLink></li>
                <li><NavLink to="/temp"><div className='btn'><span>Temperature</span></div></NavLink></li>
                <li><NavLink to="/moist"><div className='btn'><span>Moisture</span></div></NavLink></li>
              </ul>
            </nav>
        </header>

        <div className="content">
          <Route exact path="/" component={Home}/>
          <Route path="/temp" component={Temp}/>
          <Route path="/moist" component={Moist}/>
        </div>

    </HashRouter>
  );
}


export default Header;