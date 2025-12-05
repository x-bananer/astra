"use client";

import styles from './page-home.module.css';

import { useState } from "react";

import { useAuth } from "../auth/auth-provider";

import Button from '../_block/button/button';
import PageHomeCard from '../page-home/page-home-card/page-home-card';

const PageHome = () => {
    const auth = useAuth();

    const getGreeting = (user) => {
        const h = new Date().getHours();

        let text = "";
        if (h >= 5 && h < 12) text = "Good morning";
        else if (h >= 12 && h < 18) text = "Good afternoon";
        else if (h >= 18 && h < 23) text = "Good evening";
        else text = "Good night";

        const name = user?.name || "";
        return `${text} ${name.split(' ')?.[0] || name}`;
    }
    const greeting = getGreeting(auth?.user);

    const [teamNameInput, setTeamNameInput] = useState("");
    const handleCreateTeam = async () => {
        await fetch("http://localhost:4000/groups/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ name: teamNameInput })
        });
        setTeamNameInput('')
        await auth.loadUser();
    }

    const [teammateEmailInput, setTeammateEmailInput] = useState("");
    const handleAddMember = async () => {
        await fetch("http://localhost:4000/groups/add-member", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ email: teammateEmailInput })
        });
        setTeammateEmailInput('')
        await auth.loadUser();
    };

    const handleRemoveMember = async (userId) => {
        await fetch("http://localhost:4000/groups/remove-member", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ user_id: userId })
        });

        await auth.loadUser();
    };

    return (
        <div className={styles['page-home']}>
            <div className={styles['page-home__header']}>
                <h1 className={styles['page-home__title']}>{greeting}</h1>
                <p className={styles['page-home__subtitle']}>Manage your team and integrations, and learn what data ASTRA accesses</p>
            </div>
            <div className={styles['page-home__content']}>
                <div className={styles['page-home__grid']}>
                    <div className={styles['page-home__box']}>
                        {auth?.user?.id &&
                            <div className={styles['page-home__box-item--fixed']} >
                                <div className={styles['page-home__box-media']} style={{ 'marginBottom': 'auto', 'paddingBottom': '16px', 'borderBottom': '1px solid #d0d0d0' }}>
                                    <div className={styles['page-home__box-image']}>
                                        <img alt="Astra User Avatar" src={auth?.user?.avatar} />
                                    </div>
                                    {auth?.user?.name}
                                </div>
                                {auth?.user?.group_id &&
                                    <>
                                        <input
                                            type="text"
                                            placeholder="Teammate email"
                                            value={teammateEmailInput}
                                            onChange={(e) => setTeammateEmailInput(e.target.value)}
                                            className={styles['page-home__box-input']}
                                            style={{ 'marginTop': '16px' }}

                                        />
                                        <Button size="small" style={{ 'marginTop': '8px' }} variant="outline" onClick={handleAddMember}>
                                            + Add Teammate
                                        </Button>

                                    </>
                                }
                            </div>
                        }
                        <div className={styles['page-home__box-item']}>
                            <h2 className={styles['page-home__box-title']}>Your Team</h2>
                            {auth?.user?.group?.id ?
                                <>
                                    <p className={styles['page-home__box-text-secondary']}>
                                        Team name
                                    </p>
                                    {auth?.user?.group?.name}

                                    <div style={{ "marginTop": "10px" }}>
                                        <p className={styles['page-home__box-text-secondary']}>
                                            Teammates
                                        </p>

                                        <ul>
                                            {auth?.user?.group?.members.map((member, index) => (
                                                <li key={index}>
                                                    <div className={`${styles['page-home__box-media']} ${styles['page-home__box-media--small']}`}>
                                                        <div className={`${styles['page-home__box-image']} ${styles['page-home__box-image--small']}`}>
                                                            <img alt="Astra User Avatar" src={member?.avatar} />
                                                        </div>
                                                        <p>{member?.name}</p>
                                                        <Button variant="icon" style={{ 'marginLeft': '8px' }} onClick={() => handleRemoveMember(member.user_id)}>
                                                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                                                <path d="M7 5H5H3C2.44772 5 2 5.44772 2 6C2 6.55228 2.44772 7 3 7H4V20C4 21.6569 5.34315 23 7 23H17C18.6569 23 20 21.6569 20 20V7H21C21.5523 7 22 6.55228 22 6C22 5.44772 21.5523 5 21 5H19H17V4C17 2.34315 15.6569 1 14 1H10C8.34314 1 7 2.34315 7 4V5ZM9 5H15V4C15 3.44772 14.5523 3 14 3H10C9.44771 3 9 3.44772 9 4V5ZM16 7H8H6V20C6 20.5523 6.44771 21 7 21H17C17.5523 21 18 20.5523 18 20V7H16ZM9 11V17C9 17.5523 9.44771 18 10 18C10.5523 18 11 17.5523 11 17V11C11 10.4477 10.5523 10 10 10C9.44771 10 9 10.4477 9 11ZM13 17V11C13 10.4477 13.4477 10 14 10C14.5523 10 15 10.4477 15 11V17C15 17.5523 14.5523 18 14 18C13.4477 18 13 17.5523 13 17Z" fill="currentColor" />
                                                            </svg>
                                                        </Button>
                                                    </div>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                </> :
                                <>
                                    <div>
                                        You don't have a team yet. You can create a new one or ask your teammates to add you to an existing team, allowing you to set up integrations and monitor your team’s activity.
                                    </div>
                                    <input
                                        type="text"
                                        placeholder="Team name"
                                        value={teamNameInput}
                                        onChange={(e) => setTeamNameInput(e.target.value)}
                                        className={styles['page-home__box-input']}
                                        style={{ 'marginTop': '20px' }}

                                    />
                                    <Button size="small" className={styles['page-home__box-button']} variant="outline" onClick={handleCreateTeam}>
                                        + Create Team
                                    </Button>
                                </>
                            }
                        </div>
                    </div>

                    <div className={styles['page-home__box']}>
                        <div className={styles['page-home__box-item--full']}>
                            <h2 className={styles['page-home__box-title']}>Integrations</h2>

                            {auth?.user?.group?.id ?
                                <div className={styles['page-home__box-grid']}>
                                    <PageHomeCard
                                        type="github"
                                    />
                                    <PageHomeCard
                                        type="gitlab"
                                    />
                                    <PageHomeCard
                                        type="gdocs"
                                    />
                                    <PageHomeCard
                                        type="trello"
                                    />
                                </div> :
                                <div className={styles['page-home-card']}>
                                    To set up, edit, or view your integrations, you need to belong to a team.
                                    Create your own team using the "+ Create Team" button or join an existing one to start working with GitHub, GitLab, Trello, and Google Docs integrations and monitor your team’s activity..
                                </div>
                            }
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PageHome;