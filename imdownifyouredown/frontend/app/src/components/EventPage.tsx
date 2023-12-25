import { HeaderBanner, User, Event } from "./util"
import "./customTypes.css"

export function EventPage(props: {user: User, event: Event}) {
    return (
        <div>
            <HeaderBanner user={props.user} />
            <EventBody user={props.user} event={props.event} />
        </div>
    );
}


function EventBody(props: {user: User, event: Event}) {
    return (
        <div>
            <div>
                <EventBanner event={props.event} />
            </div>
            <div>
                <EventDescription event={props.event} />
            </div>
            <br/>
            <div>
                <EventUserResponse user={props.user} event={props.event} />
            </div>
            <br/>
            <div>
                <EventGuestsTable event={props.event} />
            </div>
            <br/>
            <div>
                <EventStatus event={props.event} />
            </div>
        </div>
    );
}


function EventBanner(props: {event: Event}) {
    return (
        <div className="event-banner">
            <image>
                Image Placeholder
            </image>
        </div>
    );
}


function EventDescription(props: {event: Event}) {
    return (
        <div>
            {props.event.description}
        </div>
    )
}


function EventUserResponse(props: {user: User, event: Event}) {
    return (
        <div>
            <UserPublicResponse user={props.user} event={props.event} />
            <UserPrivateResponse user={props.user} event={props.event} />
        </div>
    );
}


function UserPublicResponse(props: {user: User, event: Event}) {
    return (
        <div>
            <span>Public Response: </span>
            <button>Down</button>
            <button>Maybe</button>
            <button>Not Down</button>
        </div>
    );
}


function UserPrivateResponse(props: {user: User, event: Event}) {
    return (
        <div>
            <span>Private Response: </span>
            <button>Down</button>
            <button>Maybe</button>
            <button>Not Down</button>
        </div>
    );
}


function EventGuestsTable(props: { event: Event }) {
    const rows: Array<JSX.Element> = [];
    // const guests = fetch();
    const guests = [
        {"user_id": 1, "username": "test1", "response": "Down"},
        {"user_id": 2, "username": "test2", "response": "Down"},
        {"user_id": 3, "username": "test3", "response": "Not Down"}
    ];

    guests.forEach(e => {
        rows.push(
            <EventGuestsRow
                user_id={e.user_id}
                username={e.username}
                response={e.response}
            />
        );
    });

    return (
        <table align="center">
            <thead>
                <th>Username</th>
                <th>Reseponse</th>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    );
}


function EventGuestsRow(props: {
    user_id: number,
    username: string,
    response: string
}) {
    return (
        <tr>
            <td width="200px">{props.username}</td>
            <td width="200px">{props.response}</td>
        </tr>
    );
}


function EventStatus(props: {event: Event}) {
    return (
        <span><b>Event Status:</b> Still On!</span>
    )
}
