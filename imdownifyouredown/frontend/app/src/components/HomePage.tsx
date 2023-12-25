import {User, HeaderBanner} from "./util"


export function HomePage(props: {user: User}) {
    return (
        <header>
            <HeaderBanner user={props.user} />
        </header>
    );
}
