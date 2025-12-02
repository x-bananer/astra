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

        await auth.loadUser();
    }

    return (
        <div className={styles['page-home']}>
            <div className={styles['page-home__header']}>
                <h1 className={styles['page-home__title']}>{greeting}</h1>
            </div>
            <div className={styles['page-home__content']}>
                <div className={styles['page-home__grid']}>
                    <div className={styles['page-home__box']}>
                        {auth?.user?.id &&
                            <div className={styles['page-home__box-item']}>
                                <h2 className={styles['page-home__box-title']}>You</h2>
                                <div className={styles['page-home__box-media']}>
                                    <div className={styles['page-home__box-image']}>
                                        <img alt="Astra User Avatar" src={auth?.user?.avatar} />
                                    </div>
                                    {auth?.user?.name}
                                </div>
                            </div>
                        }
                        <div className={styles['page-home__box-item']}>
                            <h2 className={styles['page-home__box-title']}>Your Team</h2>
                            {auth?.user?.group?.id ?
                                <>
                                     Team name: {auth?.user?.group?.name}

                                    <div style={{ "marginTop": "10px" }}>
                                        Teammates:
                                        <ul>
                                            {auth?.user?.group?.members.map((member, index) => (
                                                <li key={index}>
                                                    {index + 1}. {member.name}
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                    <Button size="small" style={{ 'marginTop': '20px' }} variant="outline">
                                        + Add Teammate
                                    </Button>

                                </> :
                                <>
                                    <div>
                                        You don’t have a team yet. You can create a new one or ask your teammates to add you to an existing team, allowing you to set up integrations and monitor your team’s activity.
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