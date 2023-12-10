import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;

// App.tsx
// import React, { useState, useEffect } from 'react';
// import { BrowserRouter as Router, Route, Switch, useParams } from 'react-router-dom';

// interface Event {
//   name: string;
//   description: string;
// }

// interface User {
//   name: string;
//   email: string;
// }

// const API_BASE_URL = 'http://your-api-base-url'; // Replace with your actual API base URL

// // Component for fetching event details
// const EventDetails: React.FC<{ eventId: string }> = ({ eventId }) => {
//   const [event, setEvent] = useState<Event | null>(null);

//   useEffect(() => {
//     const fetchEvent = async () => {
//       try {
//         const response = await fetch(`${API_BASE_URL}/get_event/${eventId}`);
//         const data: Event = await response.json();
//         setEvent(data);
//       } catch (error) {
//         console.error('Error fetching event:', error);
//       }
//     };

//     fetchEvent();
//   }, [eventId]);

//   if (!event) {
//     return <div>Loading event details...</div>;
//   }

//   return (
//     <div>
//       <h2>{event.name}</h2>
//       <p>{event.description}</p>
//     </div>
//   );
// };

// // Component for fetching user details
// const UserDetails: React.FC = () => {
//   const [user, setUser] = useState<User | null>(null);

//   useEffect(() => {
//     const fetchUser = async () => {
//       try {
//         const response = await fetch(`${API_BASE_URL}/get_user`);
//         const data: User = await response.json();
//         setUser(data);
//       } catch (error) {
//         console.error('Error fetching user:', error);
//       }
//     };

//     fetchUser();
//   }, []);

//   if (!user) {
//     return <div>Loading user details...</div>;
//   }

//   return (
//     <div>
//       <h2>{user.name}</h2>
//       <p>{user.email}</p>
//     </div>
//   );
// };

// // EditEvent component with dynamic routing
// const EditEvent: React.FC = () => {
//   const { event_id } = useParams<{ event_id: string }>();
//   return <h2>Edit Event {event_id}</h2>;
// };

// // Main App component
// const App: React.FC = () => {
//   return (
//     <Router>
//       <Switch>
//         <Route path="/event/:event_id">
//           {({ match }) => <EventDetails eventId={match?.params.event_id || ''} />}
//         </Route>
//         <Route path="/edit/:event_id">
//           <EditEvent />
//         </Route>
//         <Route path="/user">
//           <UserDetails />
//         </Route>
//       </Switch>
//     </Router>
//   );
// };

// export default App;
