import { Outlet } from "react-router-dom";

const Layout = () => {
  return (
    <div>
      <header>My Persistent Header</header>
      <main>
        {/* Child routes render here */}
        <Outlet />
      </main>
      <footer>My Footer</footer>
    </div>
  );
};

export default Layout;
