import { useEffect } from "react";
import "./customTypes.css"


interface User {
    user_id: number;
    username: string;
}
interface Users extends Array<User>{};


interface Event {
  event_id: number;
  name: string;
  users: Users;
  description: string;
}


export function HeaderBanner(props: { user: User }) {
    return (
        <div className="header-banner">
            <div className="left-align">
                <HomeButton />
            </div>

            <h1>I'm Down If You're Down</h1>

            <div className="right-align">
                <UserIcon user={props.user} />
            </div>
        </div>
    );
}


function HomeButton() {
    return (
        // <button onClick={}>
        <button>
            Logo
        </button>
    );
}


function UserIcon(props: { user: User }) {
    return (
        <button>
            {props.user.username}
        </button>
    );
}


export type { User as User, Event as Event };
