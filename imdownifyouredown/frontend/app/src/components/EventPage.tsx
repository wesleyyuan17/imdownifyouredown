import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { User, Event } from "./util"
import "./customTypes.css"


async function getEventInfo(event_id: number) {
    const response = await fetch(`http://localhost:8000/events?event_id=${event_id}`)
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return response.json()
}


export function EventPage(props: {user: User}) {
    const [event, setEvent] = useState<Event>();
    const [searchParams, setSearchParams] = useSearchParams();
    const event_id = Number(searchParams.get("event_id"));

    useEffect(() => {
        getEventInfo(event_id).then(data => setEvent(data));
    }, []);

    return (event === undefined) ? (
        <div>Loading...</div>
    ) : (
        <div>
            <EventBody user={props.user} event={event} />
        </div>
    );
}


function EventBody(props: {user: User, event: Event}) {
    // const [event, setEvent] = useState<Event>(props.event);

    // useEffect(() => {
    //     setEvent(event);
    // }, [props.event]);

    // console.log(event)

    return (
        <div>
            <div>
                <EventBanner event={props.event} />
            </div>
            <div>
                <header>{props.event.eventname}</header>
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
            <a><img alt="Image Placeholder"></img></a>
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
                key={e.user_id}
                user_id={e.user_id}
                username={e.username}
                response={e.response}
            />
        );
    });

    return (
        <table align="center">
            <thead>
                <tr><th>Username</th></tr>
                <tr><th>Reseponse</th></tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
    );
}


function EventGuestsRow(props: {
    key: number,
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
