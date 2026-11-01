#include "mod_plugins.h"

#include <string.h>

static void activate_kurushi_adaptive_widescreen(void) {
    /* Begin at 16:9, then follow the game window up to 21:9. The PSX frame
     * remains 4:3 during BIOS startup; the runtime engages wide projection
     * only when the game starts. */
    (void)psx_mod_set_fixed_display_aspect(16u, 9u);
    (void)psx_mod_set_adaptive_display_aspect(21u, 9u);
}

static void activate_kurushi_fast_cd_loading(void) {
    /* 2x shortens emulated sector deadlines while keeping the game at its
     * normal speed. Keep this opt-in because earlier CD interrupts can expose
     * timing assumptions in the title. */
    (void)psx_mod_set_disc_speed(2u, 0u);
}

static void activate_kurushi_anti_aliasing(void) {
    char value[32] = "fxaa";
    uint32_t mode = 1u;
    if (psx_mod_option_value("kurushi.qol", "anti-aliasing",
                             "mode", value, sizeof value)) {
        if (!strcmp(value, "off")) mode = 0u;
        else if (!strcmp(value, "fxaa_hq")) mode = 2u;
    }
    (void)psx_mod_set_post_aa(mode);
}

static void activate_kurushi_smooth_motion(void) {
    char value[32] = "display";
    uint32_t rate = 0u;
    if (psx_mod_option_value("kurushi.qol", "smooth-motion",
                             "output-rate", value, sizeof value)) {
        if (!strcmp(value, "60")) rate = 60u;
        else if (!strcmp(value, "120")) rate = 120u;
    }
    (void)psx_mod_set_frame_interpolation_source(PSX_MOD_FRAME_SOURCE_FLIP);
    (void)psx_mod_set_frame_interpolation_blend(
        PSX_MOD_FRAME_INTERPOLATION_MOTION_ADAPTIVE);
    (void)psx_mod_set_frame_interpolation(rate);
}

PSX_MOD_CONSTRUCTOR(register_kurushi_widescreen_plugin) {
    (void)psx_mod_register_activation_plugin(
        "kurushi.widescreen.fit21",
        activate_kurushi_adaptive_widescreen);
}

PSX_MOD_CONSTRUCTOR(register_kurushi_fast_cd_plugin) {
    (void)psx_mod_register_activation_plugin(
        "kurushi.loading.cd2x",
        activate_kurushi_fast_cd_loading);
}

PSX_MOD_CONSTRUCTOR(register_kurushi_aa_plugin) {
    (void)psx_mod_register_activation_plugin(
        "kurushi.visual.anti-aliasing",
        activate_kurushi_anti_aliasing);
}

PSX_MOD_CONSTRUCTOR(register_kurushi_smooth_motion_plugin) {
    (void)psx_mod_register_activation_plugin(
        "kurushi.presentation.smooth-motion",
        activate_kurushi_smooth_motion);
}
