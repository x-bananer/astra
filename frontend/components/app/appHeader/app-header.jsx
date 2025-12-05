import { useAuth } from "../../auth/auth-provider";

import styles from './app-header.module.css';

import AppHeaderLink from './app-header-link';
import Button from '../../_block/button/button';

const AppHeader = ({ className }) => {
    const handleLogout = async () => {
        try {
            await fetch("http://localhost:4000/auth/logout", {
                method: "POST",
                credentials: "include",
            });
        } catch (e) {
            console.error(e)
        }
        window.location.href = "/login";
    };

    const auth = useAuth();

    return (
        <header className={`${styles['app-header']} ${className || ''}`}>

            <div className={styles['app-header__logo']}>
                <img src="/logo-small.svg" />
                ASTRA
            </div>

            <nav className={styles['app-header__nav']}>
                <AppHeaderLink
                    href='/'
                    className={styles['app-header__nav-link']}
                >
                    Dashboard
                </AppHeaderLink>
                <AppHeaderLink
                    href='/statistics'
                    className={styles['app-header__nav-link']}
                >
                    Statistics
                </AppHeaderLink>
                <AppHeaderLink
                    href='/analysis'
                    className={styles['app-header__nav-link']}
                >
                    ASTRA Analysis
                </AppHeaderLink>
            </nav>

            {auth?.user && auth?.user.id && 
            <div className={styles['app-header__avatar']}>
                <div className={styles['app-header__avatar-icon']}>
                    { auth?.user?.avatar ?
                        <img src={auth?.user?.avatar} alt="ASTRA User avatar" /> :
                        <span>{auth?.user?.name?.[0]}</span>
                    }
                </div>
                <div className={styles['app-header__avatar-text']}>
                    <p>{auth?.user?.name}</p>
                    {auth?.user?.group?.name ??
                    <p>{auth?.user?.group?.name}</p>}
                </div>
            </div>
            }

            {auth?.user?.id && (
                <Button
                    variant="outline"
                    size="small"
                    className={styles['app-header__button']}
                    onClick={handleLogout}
                >
                    Log Out
                </Button>
            )}
        </header>
    );
}

export default AppHeader;