import { BrowserRouter, Route, Routes } from "react-router-dom"
import { lazy, Suspense } from "react"
import Profile from "../pages/User/Profile"
import Home from "../pages/Home"

const Router = () => {
  return (
    <Suspense fallback={<h3>Loading...</h3>}>
      <BrowserRouter>
        <header className="h-20">
          {/* <Navbar /> */}
        </header>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          {/*<Route path="/men" element={<Men />} />
          <Route path="/women" element={<Women />} />
          <Route path="/accessories" element={<Accessories />} />
          <Route path="/:type/all" element={<NewsProducts />} />
          <Route path="/accessories/:category" element={<Accessory />} />
          <Route path="/:sex/:category" element={<Category />} />
          <Route path="/:type/news/gym-clothes" element={<NewsProducts />} />
          <Route path="/:type" element={<NewsProducts />} />
          <Route path="/product/:id/:colorId" element={<Product />} />
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/category/:id_category/clothes" element={<Clothes />} />
          <Route path="/terms&conditions" element={<TerminosCondiciones />} />
          <Route path="/admin/clothe-form" element={<PostNewClothe />} />
          <Route path="/admin/categories" element={<ClotheCategories />} /> */}
          {/* <Route path="/admin/categories/:categoryId" element={<AdminClothes />} /> */}
        </Routes>
        {/* <Footer /> */}
      </BrowserRouter>
    </Suspense>
  )
}

export default Router