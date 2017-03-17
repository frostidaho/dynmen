from dynmen.common import TraitMenu, Flag, Option


class Rofi(TraitMenu):
    _base_command = ['rofi']
    no_config = Flag(
        '-no-config',
        info_text='Do not load configuration, use default values.')
    version = Flag('-version', info_text='Print the version number and exit.')
    dmenu = Flag('-dmenu', default_value=True)
    display = Option(
        '-display', info_text='X server to contact. @@@ ${DISPLAY}')
    help = Flag('-help', info_text='This help message.')
    dump_xresources = Flag(
        '-dump-xresources',
        info_text='Dump the current configuration in Xresources format and exit.'
    )
    dump_xresources_theme = Flag(
        '-dump-xresources-theme',
        info_text='Dump the current color scheme in Xresources format and exit.'
    )
    e = Option(
        '-e',
        info_text='Show a dialog displaying the passed message and exit.')
    markup = Flag('-markup', info_text='Enable pango markup where possible.')
    normal_window = Flag(
        '-normal-window',
        info_text='In dmenu mode, behave as a normal window. (experimental)')
    show = Option(
        '-show',
        info_text="Show the mode 'mode' and exit. The mode has to be enabled.")
    lazy_grab = Flag(
        '-lazy-grab',
        info_text="When fail to grab keyboard, don't block but retry later.")
    mesg = Option(
        '-mesg',
        info_text='Print a small user message under the prompt (uses pango markup)'
    )
    p = Option('-p', info_text='Prompt to display left of entry field')
    selected_row = Option('-selected-row', info_text='Select row')
    format = Option('-format', info_text='Output format string @@@ s')
    u = Option('-u', info_text='List of row indexes to mark urgent')
    a = Option('-a', info_text='List of row indexes to mark active')
    l = Option('-l', info_text='Number of rows to display')
    i = Flag('-i', info_text='Set filter to be case insensitive')
    only_match = Flag(
        '-only-match', info_text='Force selection or custom entry')
    no_custom = Flag('-no-custom', info_text="Don't accept custom entry")
    select = Option('-select', info_text='Select the first row that matches')
    password = Flag(
        '-password',
        info_text="Do not show what the user inputs. Show '*' instead.")
    markup_rows = Flag(
        '-markup-rows',
        info_text='Allow and render pango markup as input data.')
    sep = Option('-sep', default_value='\x00')
    input = Option(
        '-input',
        info_text='Read input from file instead from standard input.')
    sync = Flag(
        '-sync',
        info_text='Force dmenu to first read all input data, then show dialog.')
    modi = Option(
        '-modi', info_text='Enabled modi @@@ window,run,ssh (Default)')
    width = Option('-width', info_text='Window width @@@ 50 (Default)')
    lines = Option('-lines', info_text='Number of lines @@@ 15 (Default)')
    columns = Option('-columns', info_text='Number of columns @@@ 1 (Default)')
    font = Option('-font', info_text='Font to use @@@ mono 12 (Default)')
    color_normal = Option(
        '-color-normal',
        info_text='Color scheme for normal row @@@ argb:00000000, #D8DEE9 , argb:00000000, #FAC863 , #1B2B34 (XResources)'
    )
    color_urgent = Option(
        '-color-urgent',
        info_text='Color scheme for urgent row @@@ argb:00000000, #F99157 , argb:00000000, #F99157 , #1B2B34 (XResources)'
    )
    color_active = Option(
        '-color-active',
        info_text='Color scheme for active row @@@ argb:00000000, #6699CC , argb:00000000, #6699CC , #1B2B34 (XResources)'
    )
    color_window = Option(
        '-color-window',
        info_text='Color scheme window @@@ argb:ee222222, #FAC863 , #FAC863 (XResources)'
    )
    bw = Option('-bw', info_text='Border width @@@ 1 (Default)')
    location = Option(
        '-location', info_text='Location on screen @@@ 0 (Default)')
    padding = Option('-padding', info_text='Padding @@@ 5 (Default)')
    yoffset = Option(
        '-yoffset', info_text='Y-offset relative to location @@@ 0 (Default)')
    xoffset = Option(
        '-xoffset', info_text='X-offset relative to location @@@ 0 (Default)')
    fixed_num_lines = Flag(
        '-fixed-num-lines',
        info_text='Always show number of lines @@@ True (Default)')
    no_fixed_num_lines = Flag(
        '-no-fixed-num-lines',
        info_text='Always show number of lines @@@ True (Default)')
    terminal = Option(
        '-terminal',
        info_text='Terminal to use @@@ rofi-sensible-terminal (Default)')
    ssh_client = Option(
        '-ssh-client', info_text='Ssh client to use @@@ ssh (Default)')
    ssh_command = Option(
        '-ssh-command',
        info_text='Ssh command to execute @@@ {terminal} -e {ssh-client} {host} (Default)'
    )
    run_command = Option(
        '-run-command', info_text='Run command to execute @@@ {cmd} (Default)')
    run_list_command = Option(
        '-run-list-command',
        info_text='Command to get extra run targets @@@  (Default)')
    run_shell_command = Option(
        '-run-shell-command',
        info_text='Run command to execute that runs in shell @@@ {terminal} -e {cmd} (Default)'
    )
    window_command = Option(
        '-window-command',
        info_text='Command executed on accep-entry-custom for window modus @@@ xkill -id {window} (Default)'
    )
    disable_history = Flag(
        '-disable-history',
        info_text='Disable history in run/ssh @@@ False (Default)')
    no_disable_history = Flag(
        '-no-disable-history',
        info_text='Disable history in run/ssh @@@ False (Default)')
    levenshtein_sort = Flag(
        '-levenshtein-sort',
        info_text='Use levenshtein sorting @@@ False (Default)')
    no_levenshtein_sort = Flag(
        '-no-levenshtein-sort',
        info_text='Use levenshtein sorting @@@ False (Default)')
    case_sensitive = Flag(
        '-case-sensitive',
        info_text='Set case-sensitivity @@@ False (Default)')
    no_case_sensitive = Flag(
        '-no-case-sensitive',
        info_text='Set case-sensitivity @@@ False (Default)')
    cycle = Flag(
        '-cycle',
        info_text='Cycle through the results list @@@ True (Default)')
    no_cycle = Flag(
        '-no-cycle',
        info_text='Cycle through the results list @@@ True (Default)')
    sidebar_mode = Flag(
        '-sidebar-mode', info_text='Enable sidebar-mode @@@ False (Default)')
    no_sidebar_mode = Flag(
        '-no-sidebar-mode',
        info_text='Enable sidebar-mode @@@ False (Default)')
    eh = Option('-eh', info_text='Row height (in chars) @@@ 1 (Default)')
    auto_select = Flag(
        '-auto-select',
        info_text='Enable auto select mode @@@ False (Default)')
    no_auto_select = Flag(
        '-no-auto-select',
        info_text='Enable auto select mode @@@ False (Default)')
    parse_hosts = Flag(
        '-parse-hosts',
        info_text='Parse hosts file for ssh mode @@@ False (Default)')
    no_parse_hosts = Flag(
        '-no-parse-hosts',
        info_text='Parse hosts file for ssh mode @@@ False (Default)')
    parse_known_hosts = Flag(
        '-parse-known-hosts',
        info_text='Parse known_hosts file for ssh mode @@@ True (Default)')
    no_parse_known_hosts = Flag(
        '-no-parse-known-hosts',
        info_text='Parse known_hosts file for ssh mode @@@ True (Default)')
    combi_modi = Option(
        '-combi-modi',
        info_text='Set the modi to combine in combi mode @@@ window,run (Default)'
    )
    matching = Option(
        '-matching',
        info_text='Set the matching algorithm. (normal, regex, glob, fuzzy) @@@ normal (Default)'
    )
    tokenize = Flag(
        '-tokenize', info_text='Tokenize input string @@@ True (Default)')
    no_tokenize = Flag(
        '-no-tokenize', info_text='Tokenize input string @@@ True (Default)')
    m = Option('-m', info_text='Monitor id to show on @@@ -5 (Default)')
    line_margin = Option(
        '-line-margin', info_text='Margin between rows @@@ 2 (Default)')
    line_padding = Option(
        '-line-padding', info_text='Padding within rows @@@ 1 (Default)')
    filter = Option(
        '-filter', info_text='Pre-set filter @@@ (unset) (Default)')
    separator_style = Option(
        '-separator-style',
        info_text='Separator style (none, dash, solid) @@@ solid (XResources)')
    hide_scrollbar = Flag(
        '-hide-scrollbar', info_text='Hide scroll-bar @@@ False (Default)')
    no_hide_scrollbar = Flag(
        '-no-hide-scrollbar', info_text='Hide scroll-bar @@@ False (Default)')
    fullscreen = Flag(
        '-fullscreen', info_text='Fullscreen @@@ False (Default)')
    no_fullscreen = Flag(
        '-no-fullscreen', info_text='Fullscreen @@@ False (Default)')
    fake_transparency = Flag(
        '-fake-transparency',
        info_text='Fake transparency @@@ False (Default)')
    no_fake_transparency = Flag(
        '-no-fake-transparency',
        info_text='Fake transparency @@@ False (Default)')
    dpi = Option('-dpi', info_text='DPI @@@ -1 (Default)')
    threads = Option(
        '-threads',
        info_text='Threads to use for string matching @@@ 0 (Default)')
    scrollbar_width = Option(
        '-scrollbar-width', info_text='Scrollbar width @@@ 8 (Default)')
    scroll_method = Option(
        '-scroll-method',
        info_text='Scrolling method. (0: Page, 1: Centered) @@@ 0 (Default)')
    fake_background = Option(
        '-fake-background',
        info_text='Background to use for fake transparency. (background or screenshot) @@@ screenshot (Default)'
    )
    window_format = Option(
        '-window-format',
        info_text='Window Format. w (desktop name), t (title), n (name), r (role), c (class) @@@ {w}   {c}   {t} (Default)'
    )
    click_to_exit = Flag(
        '-click-to-exit',
        info_text='Click outside the window to exit @@@ True (Default)')
    no_click_to_exit = Flag(
        '-no-click-to-exit',
        info_text='Click outside the window to exit @@@ True (Default)')
    show_match = Flag(
        '-show-match',
        info_text='Indicate how it match by underlining it. @@@ True (Default)')
    no_show_match = Flag(
        '-no-show-match',
        info_text='Indicate how it match by underlining it. @@@ True (Default)')
    pid = Option(
        '-pid',
        info_text='Pidfile location @@@ /run/user/1001/rofi.pid (Default)')
    kb_primary_paste = Option(
        '-kb-primary-paste',
        info_text='Paste primary selection @@@ Control+V,Shift+Insert (Default)'
    )
    kb_secondary_paste = Option(
        '-kb-secondary-paste',
        info_text='Paste clipboard @@@ Control+v,Insert (Default)')
    kb_clear_line = Option(
        '-kb-clear-line', info_text='Clear input line @@@ Control+w (Default)')
    kb_move_front = Option(
        '-kb-move-front',
        info_text='Beginning of line @@@ Control+a (Default)')
    kb_move_end = Option(
        '-kb-move-end', info_text='End of line @@@ Control+e (Default)')
    kb_move_word_back = Option(
        '-kb-move-word-back',
        info_text='Move back one word @@@ Alt+b (Default)')
    kb_move_word_forward = Option(
        '-kb-move-word-forward',
        info_text='Move forward one word @@@ Alt+f (Default)')
    kb_move_char_back = Option(
        '-kb-move-char-back',
        info_text='Move back one char @@@ Left,Control+b (Default)')
    kb_move_char_forward = Option(
        '-kb-move-char-forward',
        info_text='Move forward one char @@@ Right,Control+f (Default)')
    kb_remove_word_back = Option(
        '-kb-remove-word-back',
        info_text='Delete previous word @@@ Control+Alt+h,Control+BackSpace (Default)'
    )
    kb_remove_word_forward = Option(
        '-kb-remove-word-forward',
        info_text='Delete next word @@@ Control+Alt+d (Default)')
    kb_remove_char_forward = Option(
        '-kb-remove-char-forward',
        info_text='Delete next char @@@ Delete,Control+d (Default)')
    kb_remove_char_back = Option(
        '-kb-remove-char-back',
        info_text='Delete previous char @@@ BackSpace,Control+h (Default)')
    kb_remove_to_eol = Option(
        '-kb-remove-to-eol',
        info_text='Delete till the end of line @@@ Control+k (Default)')
    kb_remove_to_sol = Option(
        '-kb-remove-to-sol',
        info_text='Delete till the start of line @@@ Control+u (Default)')
    kb_accept_entry = Option(
        '-kb-accept-entry',
        info_text='Accept entry @@@ Control+j,Control+m,Return,KP_Enter (Default)'
    )
    kb_accept_custom = Option(
        '-kb-accept-custom',
        info_text='Use entered text as command (in ssh/run modi) @@@ Control+Return (Default)'
    )
    kb_accept_alt = Option(
        '-kb-accept-alt',
        info_text='Use alternate accept command. @@@ Shift+Return (Default)')
    kb_delete_entry = Option(
        '-kb-delete-entry',
        info_text='Delete entry from history @@@ Shift+Delete (Default)')
    kb_mode_next = Option(
        '-kb-mode-next',
        info_text='Switch to the next mode. @@@ Shift+Right,Control+Tab (Default)'
    )
    kb_mode_previous = Option(
        '-kb-mode-previous',
        info_text='Switch to the previous mode. @@@ Shift+Left,Control+Shift+Tab (Default)'
    )
    kb_row_left = Option(
        '-kb-row-left',
        info_text='Go to the previous column @@@ Control+Page_Up (Default)')
    kb_row_right = Option(
        '-kb-row-right',
        info_text='Go to the next column @@@ Control+Page_Down (Default)')
    kb_row_up = Option(
        '-kb-row-up',
        info_text='Select previous entry @@@ Up,Control+p,Shift+Tab,Shift+ISO_Left_Tab (Default)'
    )
    kb_row_down = Option(
        '-kb-row-down',
        info_text='Select next entry @@@ Down,Control+n (Default)')
    kb_row_tab = Option(
        '-kb-row-tab',
        info_text='Go to next row, if one left, accept it, if no left next mode. @@@ Tab (Default)'
    )
    kb_page_prev = Option(
        '-kb-page-prev',
        info_text='Go to the previous page @@@ Page_Up (Default)')
    kb_page_next = Option(
        '-kb-page-next',
        info_text='Go to the next page @@@ Page_Down (Default)')
    kb_row_first = Option(
        '-kb-row-first',
        info_text='Go to the first entry @@@ Home,KP_Home (Default)')
    kb_row_last = Option(
        '-kb-row-last',
        info_text='Go to the last entry @@@ End,KP_End (Default)')
    kb_row_select = Option(
        '-kb-row-select',
        info_text='Set selected item as input text @@@ Control+space (Default)')
    kb_screenshot = Option(
        '-kb-screenshot',
        info_text='Take a screenshot of the rofi window @@@ Alt+S (Default)')
    kb_toggle_case_sensitivity = Option(
        '-kb-toggle-case-sensitivity',
        info_text='Toggle case sensitivity @@@ grave,dead_grave (Default)')
    kb_toggle_sort = Option(
        '-kb-toggle-sort', info_text='Toggle sort @@@ Alt+grave (Default)')
    kb_cancel = Option(
        '-kb-cancel',
        info_text='Quit rofi @@@ Escape,Control+g,Control+bracketleft (Default)'
    )
    kb_custom_1 = Option(
        '-kb-custom-1', info_text='Custom keybinding 1 @@@ Alt+1 (Default)')
    kb_custom_2 = Option(
        '-kb-custom-2', info_text='Custom keybinding 2 @@@ Alt+2 (Default)')
    kb_custom_3 = Option(
        '-kb-custom-3', info_text='Custom keybinding 3 @@@ Alt+3 (Default)')
    kb_custom_4 = Option(
        '-kb-custom-4', info_text='Custom keybinding 4 @@@ Alt+4 (Default)')
    kb_custom_5 = Option(
        '-kb-custom-5', info_text='Custom Keybinding 5 @@@ Alt+5 (Default)')
    kb_custom_6 = Option(
        '-kb-custom-6', info_text='Custom keybinding 6 @@@ Alt+6 (Default)')
    kb_custom_7 = Option(
        '-kb-custom-7', info_text='Custom Keybinding 7 @@@ Alt+7 (Default)')
    kb_custom_8 = Option(
        '-kb-custom-8', info_text='Custom keybinding 8 @@@ Alt+8 (Default)')
    kb_custom_9 = Option(
        '-kb-custom-9', info_text='Custom keybinding 9 @@@ Alt+9 (Default)')
    kb_custom_10 = Option(
        '-kb-custom-10', info_text='Custom keybinding 10 @@@ Alt+0 (Default)')
    kb_custom_11 = Option(
        '-kb-custom-11',
        info_text='Custom keybinding 11 @@@ Alt+exclam (Default)')
    kb_custom_12 = Option(
        '-kb-custom-12', info_text='Custom keybinding 12 @@@ Alt+at (Default)')
    kb_custom_13 = Option(
        '-kb-custom-13',
        info_text='Csutom keybinding 13 @@@ Alt+numbersign (Default)')
    kb_custom_14 = Option(
        '-kb-custom-14',
        info_text='Custom keybinding 14 @@@ Alt+dollar (Default)')
    kb_custom_15 = Option(
        '-kb-custom-15',
        info_text='Custom keybinding 15 @@@ Alt+percent (Default)')
    kb_custom_16 = Option(
        '-kb-custom-16',
        info_text='Custom keybinding 16 @@@ Alt+dead_circumflex (Default)')
    kb_custom_17 = Option(
        '-kb-custom-17',
        info_text='Custom keybinding 17 @@@ Alt+ampersand (Default)')
    kb_custom_18 = Option(
        '-kb-custom-18',
        info_text='Custom keybinding 18 @@@ Alt+asterisk (Default)')
    kb_custom_19 = Option(
        '-kb-custom-19',
        info_text='Custom Keybinding 19 @@@ Alt+parenleft (Default)')
    display_ssh = Option(
        '-display-ssh',
        info_text='The display name of this browser @@@ (unset) (Default)')
    display_run = Option(
        '-display-run',
        info_text='The display name of this browser @@@ (unset) (Default)')
    display_drun = Option(
        '-display-drun',
        info_text='The display name of this browser @@@ (unset) (Default)')
    display_window = Option(
        '-display-window',
        info_text='The display name of this browser @@@ (unset) (Default)')
    display_windowcd = Option(
        '-display-windowcd',
        info_text='The display name of this browser @@@ (unset) (Default)')
    display_combi = Option(
        '-display-combi',
        info_text='The display name of this browser @@@ (unset) (Default)')

