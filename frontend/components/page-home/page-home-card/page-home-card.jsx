import styles from './page-home-card.module.css';

import { useState } from 'react';

import { useAuth } from '../../auth/auth-provider';

import Button from '../../_block/button/button';

const INTEGRATIONS = {
    github: {
        title: "GitHub",
        caption: "Your team doesn't have a GitHub repository connected yet. Connect one to start analyzing commit activity.",
        description: `ASTRA accesses only the repository you connect. We read:
   • commit history,
   • commit authors,
   • timestamps,
   • change statistics,
   • commit messages.
No other repositories or account data are accessed.`,
        placeholder: "Owner/Repo",
        addLabel: "+ Add GitHub Repo",
        changeLabel: "Change Repository",
        buildUrl: (v) =>
            `http://localhost:4000/auth/github/login?repo=${encodeURIComponent(v)}`,
        renderConnected: (integration, styles, handleRemoveClient) => {
            const [owner, repo] = integration.resource_ref.split("/");
            return (
                <>
                    <div className={styles['page-home-card__text']}>
                        <p className={styles['page-home-card__text-gray']} style={{ 'display': 'flex', 'alignItems': 'center' }}>
                            Connected repository
                            <Button variant="icon" style={{ 'marginLeft': '8px' }} onClick={() => handleRemoveClient('github')}>
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M7 5H5H3C2.44772 5 2 5.44772 2 6C2 6.55228 2.44772 7 3 7H4V20C4 21.6569 5.34315 23 7 23H17C18.6569 23 20 21.6569 20 20V7H21C21.5523 7 22 6.55228 22 6C22 5.44772 21.5523 5 21 5H19H17V4C17 2.34315 15.6569 1 14 1H10C8.34314 1 7 2.34315 7 4V5ZM9 5H15V4C15 3.44772 14.5523 3 14 3H10C9.44771 3 9 3.44772 9 4V5ZM16 7H8H6V20C6 20.5523 6.44771 21 7 21H17C17.5523 21 18 20.5523 18 20V7H16ZM9 11V17C9 17.5523 9.44771 18 10 18C10.5523 18 11 17.5523 11 17V11C11 10.4477 10.5523 10 10 10C9.44771 10 9 10.4477 9 11ZM13 17V11C13 10.4477 13.4477 10 14 10C14.5523 10 15 10.4477 15 11V17C15 17.5523 14.5523 18 14 18C13.4477 18 13 17.5523 13 17Z" fill="currentColor" />
                                </svg>
                            </Button>
                        </p>
                        <div className={styles['page-home-card__text-accent']}>
                            {repo}
                        </div>
                    </div>
                    <div className={styles['page-home-card__text']}>
                        <p className={styles['page-home-card__text-gray']}>
                            Owner
                        </p>
                        <p className={styles['page-home-card__text-accent']}>
                            {owner}
                        </p>
                    </div>

                </>
            );
        }
    },

    gitlab: {
        title: "GitLab",
        caption: "Your team doesn't have a GitLab project connected yet. Connect one to start analyzing commit activity.",
        description: `ASTRA accesses only the selected GitLab project. We read:
   • commit history,
   • commit authors,
   • timestamps,
   • change statistics,
   • commit messages.
No other projects or account data are accessed.`,
        placeholder: "Owner/Project",
        addLabel: "+ Add GitLab Project",
        changeLabel: "Change Project",
        buildUrl: (v) =>
            `http://localhost:4000/auth/gitlab/login?repo=${encodeURIComponent(v)}`,
        renderConnected: (integration, styles, handleRemoveClient) => {
            const [owner, repo] = integration.resource_ref.split("/");
            return (
                <>
                    <div className={styles['page-home-card__text']}>
                        <p className={styles['page-home-card__text-gray']} style={{ 'display': 'flex', 'alignItems': 'center' }}>
                            Connected project
                            <Button variant="icon" style={{ 'marginLeft': '8px' }} onClick={() => handleRemoveClient('gitlab')}>
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M7 5H5H3C2.44772 5 2 5.44772 2 6C2 6.55228 2.44772 7 3 7H4V20C4 21.6569 5.34315 23 7 23H17C18.6569 23 20 21.6569 20 20V7H21C21.5523 7 22 6.55228 22 6C22 5.44772 21.5523 5 21 5H19H17V4C17 2.34315 15.6569 1 14 1H10C8.34314 1 7 2.34315 7 4V5ZM9 5H15V4C15 3.44772 14.5523 3 14 3H10C9.44771 3 9 3.44772 9 4V5ZM16 7H8H6V20C6 20.5523 6.44771 21 7 21H17C17.5523 21 18 20.5523 18 20V7H16ZM9 11V17C9 17.5523 9.44771 18 10 18C10.5523 18 11 17.5523 11 17V11C11 10.4477 10.5523 10 10 10C9.44771 10 9 10.4477 9 11ZM13 17V11C13 10.4477 13.4477 10 14 10C14.5523 10 15 10.4477 15 11V17C15 17.5523 14.5523 18 14 18C13.4477 18 13 17.5523 13 17Z" fill="currentColor" />
                                </svg>
                            </Button>
                        </p>
                        <div className={styles['page-home-card__text-accent']}>
                            {repo}
                        </div>
                    </div>
                    <div className={styles['page-home-card__text']}>
                        <p className={styles['page-home-card__text-gray']}>
                            Owner:
                        </p>
                        <p className={styles['page-home-card__text-accent']}>
                            {owner}
                        </p>
                    </div>



                </>
            );
        }
    },

    gdocs: {
        title: "Google Docs",
        caption: "Your team doesn't have a Google Docs file connected yet. Connect one to start tracking document revisions.",
        description: `ASTRA accesses only the specific Google Docs file you choose. We read:
   • revision history,
   • authors of each revision,
   • timestamps,
   • basic document metadata.
The document's content is not read, and no other Drive files are accessed.`,
        placeholder: 'Link',
        addLabel: "+ Add Link",
        changeLabel: "Change Link",
        buildUrl: (v) =>
            `http://localhost:4000/auth/gdocs/login?doc=${encodeURIComponent(v)}`,
        renderConnected: (integration, styles, handleRemoveClient) => {
            const id = integration.resource_ref;
            return (
                <div className={styles['page-home-card__text']}>
                    <p className={styles['page-home-card__text-gray']} style={{ 'display': 'flex', 'alignItems': 'center' }}>
                        Connected document
                        <Button variant="icon" style={{ 'marginLeft': '8px' }} onClick={() => handleRemoveClient('gdocs')}>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M7 5H5H3C2.44772 5 2 5.44772 2 6C2 6.55228 2.44772 7 3 7H4V20C4 21.6569 5.34315 23 7 23H17C18.6569 23 20 21.6569 20 20V7H21C21.5523 7 22 6.55228 22 6C22 5.44772 21.5523 5 21 5H19H17V4C17 2.34315 15.6569 1 14 1H10C8.34314 1 7 2.34315 7 4V5ZM9 5H15V4C15 3.44772 14.5523 3 14 3H10C9.44771 3 9 3.44772 9 4V5ZM16 7H8H6V20C6 20.5523 6.44771 21 7 21H17C17.5523 21 18 20.5523 18 20V7H16ZM9 11V17C9 17.5523 9.44771 18 10 18C10.5523 18 11 17.5523 11 17V11C11 10.4477 10.5523 10 10 10C9.44771 10 9 10.4477 9 11ZM13 17V11C13 10.4477 13.4477 10 14 10C14.5523 10 15 10.4477 15 11V17C15 17.5523 14.5523 18 14 18C13.4477 18 13 17.5523 13 17Z" fill="currentColor" />
                            </svg>
                        </Button>
                    </p>
                    <span className={styles['page-home-card__text-accent']}>
                        <a
                            target="_blank"
                            href={`https://docs.google.com/document/d/${id}/view`}
                        >
                            https://docs.google.com/do...
                        </a>
                    </span>
                </div>
            );
        }
    },

    trello: {
        title: "Trello",
        description: "Trello integration is coming soon – we're actively building it right now!",
        placeholder: null,
        addLabel: null,
        changeLabel: null,
        buildUrl: null,
        renderConnected: null
    }
};

const PageHomeCard = ({
    type
}) => {
    const auth = useAuth();
    const integration = auth?.user?.group?.integrations?.find(i => i.provider === type);
    const [inputValue, setInputValue] = useState("");

    const config = INTEGRATIONS[type];
    const isConnected = Boolean(integration);

    const title = config.title;
    const description = config.description;
    const placeholder = config.placeholder;

    const buttonLabel = isConnected ? config.changeLabel : config.addLabel;
    const buttonVariant = isConnected ? "outline" : "primary";

    const handleRemoveClient = async (provider) => {
        await fetch("http://localhost:4000/groups/remove-client", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ provider })
        });

        await auth.loadUser();
    }

    const connectedBlock = isConnected
        ? config.renderConnected(integration, styles, handleRemoveClient)
        : null;

    const handleSubmit = () => {
        if (!config.buildUrl) return;
        const trimmed = inputValue.trim();
        if (!trimmed) return;
        window.location.href = config.buildUrl(trimmed);
    };



    return (
        <div className={styles['page-home-card']}>

            <div className={styles['page-home-card__title']}>
                {title}
            </div>

            <div style={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                {!isConnected && (
                    <span className={`${styles['page-home-card__text-secondary']} ${styles['page-home-card__description']}`}>
                        {description}
                    </span>
                )}


                {connectedBlock && (
                    <div style={{ marginTop: '4px' }}>
                        {connectedBlock}
                    </div>
                )}

                <div style={{ marginTop: 'auto', paddingTop: '12px' }}>
                    {placeholder && (
                        <input
                            type="text"
                            placeholder={placeholder}
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            className={styles['page-home-card__input']}
                            style={{ marginTop: '10px' }}
                        />
                    )}

                    {buttonLabel && (
                        <Button
                            size="small"
                            className={styles['page-home-card__button']}
                            style={{ marginTop: placeholder ? '8px' : '0' }}
                            variant={buttonVariant}
                            onClick={handleSubmit}
                        >
                            {buttonLabel}
                        </Button>
                    )}
                </div>

            </div>
        </div>
    );
}

export default PageHomeCard;