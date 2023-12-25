import React from 'react';
import logo from './logo.svg';
import './App.css';

import {HomePage} from "./components/HomePage"
import {User, Event} from "./components/util"
import { EventPage } from './components/EventPage';

function App() {
  const user: User = { user_id: 1, username: "User" };
  const event: Event = { event_id: 1, name: "TestEvent", users: [user, user] }
  return (
    <div className="App">
      {/* <HomePage user={user} /> */}
      <EventPage user={user} event={event} />
    </div>
  );
}

export default App;

// const App: React.FC = () => {
//   return (
//     <Router>
//       <div>
//         {/* Render the HeaderBanner component on every page */}
//         <HeaderBanner />

//         {/* Use Switch to render only the first matching Route */}
//         <Switch>
//           <Route path="/home" component={HomePage} />
//           <Route path="/events" component={EventPage} />
//           <Route path="/user" component={UserPage} />

//           {/* Redirect to the home page if no route matches */}
//           <Redirect to="/home" />
//         </Switch>
//       </div>
//     </Router>
//   );
// };

// export default App;
