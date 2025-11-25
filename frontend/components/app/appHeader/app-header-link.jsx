"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Button from "../../_block/button/button";

const AppHeaderLink = ({ href, className, children }) => {
    const pathname = usePathname();
    const isActive = pathname === href;

    return (
        <Link href={href}>
            <Button className={className} variant="link" active={isActive}>
                {children}
            </Button>
        </Link>
    );
}

export default AppHeaderLink;