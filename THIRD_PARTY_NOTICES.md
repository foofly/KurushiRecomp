# Third-party notices

- The Linux x64 AppImage contains the AppImage Type 2 runtime. The runtime is distributed under the MIT License; its source repository lists additional notices for statically linked musl, libfuse, squashfuse, libzstd, and zlib components: [AppImage Type 2 runtime license and notices](https://github.com/AppImage/type2-runtime/blob/main/LICENSE). AppImageKit states its license applies to its software and not to applications packaged in AppImages: [AppImageKit license](https://github.com/AppImage/AppImageKit/blob/main/LICENSE).

  MIT License (AppImage Type 2 runtime), Copyright (c) 2004-23 probonopd:

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.

This project uses the following separately licensed components:

- **PSXRecomp** is included as the `psxrecomp` submodule. Its license is in `psxrecomp/LICENSE` (PolyForm Noncommercial 1.0.0).
- **recomp-ui** is included as the `recomp-ui` submodule. Its license is in `recomp-ui/LICENSE` (MIT).
- `assets/psxrecomp.ico`, `assets/psxrecomp.png`, and `assets/psxrecomp.svg` are copies of the PSXRecomp project icon. Their license and copyright follow the PSXRecomp project; see its `LICENSE` file.
- Release archives for Windows, Linux x64, and macOS bundle the matching `cmake-clang-v1` toolchain from [RetroPorting Toolchains](https://github.com/RetroPortingToolKit/RetroPorting-Toolchains). Its compiler, build tools, and libraries remain under their individual upstream licenses. The bundled `toolchain/README.md` and `toolchain/NOTICE` identify those components and include their notices.

The original Kurushi game assets are not included. This project does not grant rights to the game or to any disc-derived material generated locally during a build.

The repository's root `LICENSE` applies only to original project-authored material that the project owner has rights to license. It does not replace the separate licenses above.
